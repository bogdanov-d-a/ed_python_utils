from __future__ import annotations
from typing import Callable


def mkdir(path_: str) -> None:
    from os import mkdir
    from os.path import exists

    if exists(path_):
        raise Exception(path_ + ' exists')

    mkdir(path_)


def remove(path_: str) -> None:
    while True:
        from os.path import exists

        print('Proceed to remove ' + path_)
        input()

        if not exists(path_):
            print(path_ + ' is already gone')
            return

        try:
            from os import rmdir
            rmdir(path_)
            return

        except:
            pass


def run_with_path(path_: str, fn: Callable[[str], None]) -> None:
    mkdir(path_)

    try:
        fn(path_)
    finally:
        remove(path_)


class PathKeeper:
    def __init__(self: PathKeeper, path: str) -> None:
        self._path = path

    def __enter__(self: PathKeeper) -> None:
        mkdir(self._path)

    def __exit__(self: PathKeeper, exc_type, exc_value, exc_tb) -> None:
        remove(self._path)
