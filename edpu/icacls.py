ICACLS = 'icacls'


def _run(args: list[str]) -> None:
    from subprocess import run
    run(args, check=True)


def icacls_view_args(path: str) -> list[str]:
    return [
        ICACLS,
        path,
    ]


def icacls_view_run(path: str) -> None:
    _run(icacls_view_args(path))


def icacls_reset_args(path: str) -> list[str]:
    return [
        ICACLS,
        path,
        '/reset',
        '/t',
        '/c',
        '/l',
        '/q',
    ]


def icacls_reset_run(path: str) -> None:
    _run(icacls_reset_args(path))
