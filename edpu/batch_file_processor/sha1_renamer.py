from typing import Optional


def exec_(src_dir: str, dst_dir: str, name_length: Optional[int]=None, keep_name: bool=False) -> None:
    from .walker import walk

    def processor(src_name: str) -> None:
        from . import utils
        from edpu.file_hashing import sha1_file
        from os import rename

        src_path = utils.path_join(src_dir, src_name)
        ext = utils.get_ext(src_name)
        dst_name = sha1_file(src_path)

        if name_length is not None:
            dst_name = dst_name[:name_length]

        if keep_name:
            dst_name += f' {utils.remove_ext(src_name)}'

        rename(src_path, utils.path_join(dst_dir, dst_name + ext))

    walk(src_dir, dst_dir, processor)
