from __future__ import annotations


WSL = 'wsl'


def _popen(cmd: str) -> None:
    from subprocess import Popen, DETACHED_PROCESS

    with Popen(cmd, creationflags=DETACHED_PROCESS) as process:
        process.communicate()


def wsl() -> None:
    _popen(WSL)


def wsl_shutdown() -> None:
    from .string_utils import merge_with_space

    _popen(merge_with_space([
        WSL,
        '--shutdown',
    ]))


class WslKeeper:
    def __init__(self: WslKeeper) -> None:
        pass

    def __enter__(self: WslKeeper) -> None:
        wsl()

    def __exit__(self: WslKeeper, exc_type, exc_value, exc_tb) -> None:
        wsl_shutdown()
