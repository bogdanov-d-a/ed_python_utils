from __future__ import annotations


EXPLORER_EXE = 'explorer.exe'


def explorer_kill() -> None:
    from .taskkill import taskkill_f_im
    taskkill_f_im(EXPLORER_EXE)


def explorer_start() -> None:
    from .string_utils import merge_with_space
    from os import system

    system(merge_with_space([
        'start',
        EXPLORER_EXE
    ]))


class ExplorerDown:
    def __init__(self: ExplorerDown) -> None:
        pass

    def __enter__(self: ExplorerDown) -> None:
        explorer_kill()

    def __exit__(self: ExplorerDown, exc_type, exc_value, exc_tb) -> None:
        explorer_start()
