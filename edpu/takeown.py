def takeown_recursive_args(path: str) -> list[str]:
    return [
        'takeown',
        '/f',
        path,
        '/r',
        '/d',
        'Y',
    ]


def takeown_recursive_run(path: str) -> None:
    from subprocess import run

    run(
        takeown_recursive_args(path),
        check=True
    )
