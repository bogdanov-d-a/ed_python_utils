def hash_file(path: str) -> str:
    from edpu.file_hashing import sha512_file

    print('Calculating hash for ' + path)
    return sha512_file(path)


def makedirs_helper(path: list[str], root: str, is_file: bool) -> None:
    from .path import path_to_root
    from os import makedirs

    if is_file:
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
