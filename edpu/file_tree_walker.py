from typing import Callable


TYPE_DIR = 'dir'
TYPE_FILE = 'file'


def walk(root_path: str,
         ignore_callback: Callable[[str, list[str]], bool]=lambda *_: False,
         file_progress: Callable[[int], None]=lambda _: None
         ) -> dict[str, list[list[str]]]:
    from os import sep
    from os import walk as os_walk
    from os.path import isdir, relpath

    if not isdir(root_path):
        raise Exception(root_path + ' does not exist')

    result: dict[str, list[list[str]]] = { TYPE_DIR: [], TYPE_FILE: [] }

    for cur_root_path, dirs, files in os_walk(root_path):
        rel_path_text = relpath(cur_root_path, root_path)

        if rel_path_text == '.':
            rel_path = []
        else:
            rel_path = rel_path_text.split(sep)

        def handler(elems: list[str], type: str) -> None:
            if type == TYPE_FILE:
                file_progress(len(elems))

            for elem in elems:
                if not ignore_callback(type, rel_path + [elem]):
                    result[type].append(rel_path + [elem])

        handler(dirs, TYPE_DIR)
        handler(files, TYPE_FILE)

    return result


def walk_type(root_path: str,
              type: str,
              ignore_callback: Callable[[list[str]], bool]=lambda *_: False,
              file_progress: Callable[[int], None]=lambda _: None
              ) -> list[list[str]]:
    return walk(
        root_path,
        lambda type_, path: type_ != type or ignore_callback(path),
        file_progress
    )[type]
