from ...context_manager import DummyContextManager
from . import time
from typing import Any


def hash_file(path: str, collector: time.Collector) -> str:
    from .mp_global import print_lock

    with print_lock():
        print('Calculating hash for ' + path)

    with time.get_perf_counter_measure(collector, time.Key.WORKER1_HASH_FILE):
        from edpu.file_hashing import sha512_file
        return sha512_file(path)


def makedirs_helper(path: list[str], root: str, type: str) -> None:
    from .mappers.type_isfile import type_to_isfile
    from .path import path_to_root
    from os import makedirs

    if type_to_isfile(type):
        if len(path) <= 1:
            return
        path = path[:-1]

    makedirs(path_to_root(path, root), exist_ok=True)


def copy_no_overwrite(src: str, dst: str, need_print: bool=False, context_manager: Any=DummyContextManager()) -> None:
    from os.path import exists

    if exists(dst):
        raise Exception('copy_no_overwrite')

    if need_print:
        from .mp_global import print_lock

        with print_lock():
            print('Copying ' + src + ' to ' + dst)

    with context_manager:
        from shutil import copy
        copy(src, dst)
