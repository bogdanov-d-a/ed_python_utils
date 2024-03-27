from __future__ import annotations


NET = 'net'
USE = 'use'


def net_use(drive: str, path: str) -> None:
    from .string_utils import merge_with_space, quotation_mark_wrap
    from os import system

    system(merge_with_space([
        NET,
        USE,
        drive,
        quotation_mark_wrap(path),
    ]))


def net_use_delete(drive: str) -> None:
    from .string_utils import merge_with_space
    from os import system

    system(merge_with_space([
        NET,
        USE,
        drive,
        '/Delete',
    ]))


class NetUseKeeper:
    def __init__(self: NetUseKeeper, drive: str, path: str) -> None:
        self._drive = drive
        self._path = path

    def __enter__(self: NetUseKeeper) -> None:
        net_use(self._drive, self._path)

    def __exit__(self: NetUseKeeper, exc_type, exc_value, exc_tb) -> None:
        net_use_delete(self._drive)
