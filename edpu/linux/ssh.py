SSH = 'ssh'


def ssh_connect(host: str) -> str:
    from ..string_utils import merge_with_space
    from .root import root

    return merge_with_space([
        SSH,
        '-l',
        root(),
        host,
    ])
