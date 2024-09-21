SSH = 'ssh'


def ssh_user(user: str) -> list[str]:
    return [
        '-l',
        user,
    ]


def ssh_dont_store_keys() -> list[str]:
    from ..string_utils import quotation_mark_wrap

    return [
        '-o',
        quotation_mark_wrap('UserKnownHostsFile=/dev/null'),
    ]


def ssh(host: str, options: list[str]) -> str:
    from ..string_utils import merge_with_space
    return merge_with_space([SSH] + options + [host])
