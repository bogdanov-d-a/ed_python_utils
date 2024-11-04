from typing import Callable


MAX_PATH = 256


def max_path_find(root: str, exclude: Callable[[str], bool]) -> None:
    from .ibds.utils.file_tree_scanner import scan
    from os import sep
    from os.path import join

    for path in filter(
        lambda path: len(path) > MAX_PATH and not exclude(path),
        map(
            lambda path: join(root, sep.join(path)),
            scan(root, [], False)
        )
    ):
        print(path)
