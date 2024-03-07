from . import time


def hash_file(path: str, collector: time.Collector) -> str:
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


def copy_no_overwrite(src: str, dst: str) -> None:
    from os.path import exists
    from shutil import copy

    if exists(dst):
        raise Exception('copy_no_overwrite')

    copy(src, dst)
