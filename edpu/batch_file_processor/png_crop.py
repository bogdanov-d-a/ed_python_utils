def _conv(src: str, dst: str, box: tuple[int, int, int, int]) -> None:
    from PIL import Image

    Image\
        .open(src)\
        .crop(box)\
        .save(dst)


def exec_(src_dir: str, dst_dir: str, box: tuple[int, int, int, int]) -> None:
    from .walker import walk

    def processor(src_name: str) -> None:
        from . import utils

        src_path = utils.path_join(src_dir, src_name)
        dst_path = utils.path_join(dst_dir, src_name)

        _conv(src_path, dst_path, box)

    walk(src_dir, dst_dir, processor)
