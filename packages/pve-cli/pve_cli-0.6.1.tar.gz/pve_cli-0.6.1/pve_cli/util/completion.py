import typer

from ..proxmox.api import Proxmox


def cluster_complete(ctx: typer.Context, incomplete: str):
    config = ctx.obj['config']
    clusters = config.get('clusters', {})
    for cluster_name in clusters:
        if cluster_name.startswith(incomplete):
            yield cluster_name, clusters[cluster_name]['host']


def vm_complete(ctx: typer.Context, incomplete: str):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    vms = proxmox_api.vm.list()

    for vm in vms:
        yield str(vm['vmid']), vm['name']
        yield vm['name'], vm['name']


def node_complete(ctx: typer.Context, incomplete: str):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    nodes = proxmox_api.node.list()

    for node in nodes:
        if node['node'].startswith(incomplete):
            yield node['node'], node['node']
