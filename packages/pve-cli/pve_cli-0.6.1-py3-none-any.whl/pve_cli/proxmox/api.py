import base64
import time
from operator import itemgetter
from pathlib import Path
from typing import Optional, Union

from proxmoxer import ProxmoxAPI
from requests.exceptions import ConnectionError

from .exceptions import (
    ProxmoxConnectionError,
    ProxmoxError,
    ProxmoxMissingPermissionError,
    ProxmoxNodeNotFoundError,
    ProxmoxVMNotFoundError,
)
from .types import ExecStatus


class ProxmoxNode:
    def __init__(self, proxmox_api: ProxmoxAPI):
        self._api = proxmox_api

    def list(self) -> list:
        nodes = self._api.nodes.get()
        return sorted(nodes, key=itemgetter('node'))

    def get(self, node: str) -> dict:
        nodes = self.list()
        for node_dict in nodes:
            if node_dict['node'] == node:
                return dict(node_dict)
        raise ProxmoxNodeNotFoundError(f'Node {node} was not found.')

    def reboot(self, node: str):
        self._api.nodes(node).status.post(command='reboot')

    def task_status(self, node: str, upid: str) -> dict:
        status = self._api.nodes(node).tasks(upid).status.get()
        return dict(status)


class ProxmoxVM:
    def __init__(self, proxmox_api: ProxmoxAPI):
        self._api = proxmox_api

        self.agent = ProxmoxVMAgent(proxmox_api)

    def list(self) -> list:
        vms = self._api.cluster.resources.get(type='vm')
        return sorted(vms, key=itemgetter('vmid'))

    def get(self, vm_identifier: Union[str, int]) -> dict:
        vm_list = self._api.cluster.resources.get(type='vm')

        if isinstance(vm_identifier, int) or vm_identifier.isdigit():
            vm_ = [vm for vm in vm_list if vm['vmid'] == int(vm_identifier)]
        elif isinstance(vm_identifier, str):
            vm_ = [vm_obj for vm_obj in vm_list if vm_obj['name'] == vm_identifier]
        else:
            raise ProxmoxError('Neither integer nor string was passed as vm identifier.')

        if len(vm_) == 0:
            raise ProxmoxVMNotFoundError(vm_identifier)

        return dict(vm_[0])

    def status(self, node: str, vm_id: int) -> dict:
        return dict(self._api.nodes(node).qemu(vm_id).status.current.get())

    def migrate_check(self, node: str, vm_id: int, target: Optional[str] = None) -> dict:
        if target is None:
            return dict(self._api.nodes(node).qemu(vm_id).migrate.get())
        return dict(self._api.nodes(node).qemu(vm_id).migrate.get(target=target))

    def migrate(self, node: str, vm_id: int, target_node: str, online: bool = True) -> str:
        upid = self._api.nodes(node).qemu(vm_id).migrate.post(target=target_node, online=1 if online else 0)
        return str(upid)

    def start(self, node: str, vm_id: int) -> str:
        return str(self._api.nodes(node).qemu(vm_id).status.start.post())

    def stop(self, node: str, vm_id: int, force: bool = False) -> str:
        return str(self._api.nodes(node).qemu(vm_id).status.shutdown.post(forceStop=1 if force else 0))

    def restart(self, node: str, vm_id: int) -> str:
        return str(self._api.nodes(node).qemu(vm_id).status.reboot.post())


class ProxmoxVMAgent:
    def __init__(self, proxmox_api: ProxmoxAPI):
        self._api = proxmox_api

    def network_interfaces(self, node: str, vm_id: int) -> list:
        res = self._api.nodes(node).qemu(vm_id).agent('network-get-interfaces').get()
        return list(res['result'])

    def execute(self, node: str, vm_id: int, command: str) -> int:
        exec_res = self._api.nodes(node).qemu(vm_id).agent.exec.post(command=command)
        return int(exec_res['pid'])

    def check_exec_status(self, node: str, vm_id: int, pid: int, timeout: int = 120) -> ExecStatus:
        start = time.time()
        now = time.time()

        while now - start < timeout:
            exec_status = self._api.nodes(node).qemu(vm_id).agent('exec-status').get(pid=pid)
            if exec_status.get('exited', 0) == 1:
                return ExecStatus(exitcode=exec_status.get('exitcode'), out_data=exec_status.get('out-data'))

            time.sleep(1)
            continue

        raise TimeoutError(f'Could not get result of process {pid} on {vm_id} within {timeout} seconds.')

    def file_write(self, node: str, vm_id: int, file_path: Path, content: bytes):
        content_encoded = base64.b64encode(content)
        self._api.nodes(node).qemu(vm_id).agent('file-write').post(content=content_encoded, file=file_path, encode=0)


class Proxmox:
    node: ProxmoxNode
    vm: ProxmoxVM

    def __init__(
        self,
        host: str,
        user: str,
        realm: str,
        token_name: str,
        token_secret: str,
        verify_ssl: Union[bool, str] = True,
        **kwargs: dict,
    ):
        self._api = ProxmoxAPI(
            host=host, user=f'{user}@{realm}', token_name=token_name, token_value=token_secret, verify_ssl=verify_ssl, **kwargs
        )

        try:
            self._api.version.get()
        except ConnectionError as exc:
            raise ProxmoxConnectionError(f'Could not connect to Proxmox API at {self._api._backend.get_base_url()}') from exc

        self.node = ProxmoxNode(proxmox_api=self._api)
        self.vm = ProxmoxVM(proxmox_api=self._api)

    def check_permission(self, path: str, permission: str):
        permissions = self._api.access.permissions.get(path=path)[path]
        if permission not in permissions:
            raise ProxmoxMissingPermissionError(path, permission)
