import inspect

import typer

from .exceptions import InvalidConfigError
from ..proxmox import Proxmox
from ..proxmox.exceptions import ProxmoxNodeNotFoundError


def cluster_validate(config: dict, cluster: str):
    clusters = config.get('clusters', {})
    if cluster not in clusters:
        raise typer.BadParameter(
            f'Config for cluster "{cluster}" could not be found in configured clusters: {", ".join(clusters)}.'
        )


def config_validate(config: dict):
    cluster_configs = config.get('clusters', {})
    default_cluster = config.get('defaults', {}).get('cluster', None)
    if default_cluster is not None and default_cluster not in cluster_configs:
        raise InvalidConfigError(
            f'The configured default cluster "{default_cluster}" '
            f'has no configuration section in the config. (available: {", ".join(cluster_configs)})'
        )

    required_keys = [
        param.name
        for param in inspect.signature(Proxmox.__init__).parameters.values()
        if param.default == inspect.Parameter.empty and param.name not in ['self', 'kwargs']
    ]

    invalid_cluster_config = False
    err_msg = []
    for cluster_name, cluster_config in cluster_configs.items():
        missing_keys = [key for key in required_keys if key not in cluster_config]
        if missing_keys:
            err_msg.append(f'  {cluster_name}: {", ".join(missing_keys)}')
            invalid_cluster_config = True

    if invalid_cluster_config:
        raise InvalidConfigError('Missing keys in config for clusters:\n{}'.format('\n'.join(err_msg)))


def node_validate(ctx: typer.Context, node: str) -> str:
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    try:
        proxmox_api.node.get(node)
    except ProxmoxNodeNotFoundError as err:
        raise typer.BadParameter(f'Node {node} does not exist.') from err
    return node
