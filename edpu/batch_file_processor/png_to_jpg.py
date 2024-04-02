def _conv(src: str, dst: str, q: int) -> None:
    from PIL import Image

    Image\
        .open(src)\
        .convert('RGB')\
        .save(dst, quality=q, optimize=True, progressive=False)


def exec_(src_dir: str, dst_dir: str, quality: int=90) -> None:
    from .walker import walk

    def processor(src_name: str) -> None:
        from . import utils

        src_path = utils.path_join(src_dir, src_name)
        dst_name = utils.remove_ext(src_name) + '.jpg'
        dst_path = utils.path_join(dst_dir, dst_name)

        _conv(src_path, dst_path, quality)

    walk(src_dir, dst_dir, processor)
