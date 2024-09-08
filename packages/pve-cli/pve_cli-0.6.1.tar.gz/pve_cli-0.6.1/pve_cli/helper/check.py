from proxmoxer import ResourceException

from ..proxmox import Proxmox
from ..util.exceptions import PVECLIError


def check_vm_migrate(proxmox_api: Proxmox, vm: dict, dest_node: str):
    try:
        migrate_check_result = proxmox_api.vm.migrate_check(node=vm['node'], vm_id=vm['vmid'], target=dest_node)
    except ResourceException as err:
        raise PVECLIError(f'Can not migrate VM {vm["name"]} ({vm["vmid"]}): {err.content}') from err
    if migrate_check_result['local_disks']:
        local_disks = [f'{disk["drivename"]} ({disk["volid"]})' for disk in migrate_check_result['local_disks']]
        raise PVECLIError(f'Can not migrate VM {vm["name"]} ({vm["vmid"]}) because of local disks {", ".join(local_disks)}.')
    if migrate_check_result['local_resources']:
        raise PVECLIError(
            f'Can not migrate VM {vm["name"]} ({vm["vmid"]}) '
            f'gbecause of local resources {migrate_check_result["local_resources"]}.'
        )
    if vm['status'] == 'stopped' and dest_node not in migrate_check_result['allowed_nodes']:
        raise PVECLIError(
            f'Can not migrate VM {vm["name"]} ({vm["vmid"]}). '
            f'Migration to {dest_node} is not allowed because of {migrate_check_result["not_allowed_nodes"][dest_node]}.'
        )
