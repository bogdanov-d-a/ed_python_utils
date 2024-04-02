from typing import Optional


def complete_name(name: str, name_length: int) -> str:
    missing = name_length - len(name)

    if missing > 0:
        name = '0' * missing + name

    return name


def exec_(src_dir: str, dst_dir: str, index: int = 0, name_length: Optional[int]=None) -> None:
    from .walker import walk

    def processor(src_name: str) -> None:
        from . import utils
        from os import rename

        nonlocal index

        src_path = utils.path_join(src_dir, src_name)
        ext = utils.get_ext(src_name)
        dst_name = str(index)

        index += 1

        if name_length is not None:
            dst_name = complete_name(dst_name, name_length)

        rename(src_path, utils.path_join(dst_dir, dst_name + ext))

    walk(src_dir, dst_dir, processor)
