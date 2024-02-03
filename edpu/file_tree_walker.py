import os
from typing import Callable


TYPE_DIR = 'dir'
TYPE_FILE = 'file'


def walk(root_path: str, ignore_callback: Callable[[str, list[str]], bool]=lambda *_: False) -> dict[str, list[list[str]]]:
    if not os.path.isdir(root_path):
        raise Exception(root_path + ' does not exist')

    result: dict[str, list[list[str]]] = { TYPE_DIR: [], TYPE_FILE: [] }

    print('Walking dir ' + root_path)
    file_count = 0

    for cur_root_path, dirs, files in os.walk(root_path):
        rel_path_text = os.path.relpath(cur_root_path, root_path)

        if rel_path_text == '.':
            rel_path = []
        else:
            rel_path = rel_path_text.split(os.sep)

        def handler(elems: list[str], type: str) -> None:
            nonlocal file_count

            if type == TYPE_FILE:
                file_count += len(elems)

            for elem in elems:
                if not ignore_callback(type, rel_path + [elem]):
                    result[type].append(rel_path + [elem])

        handler(dirs, TYPE_DIR)
        handler(files, TYPE_FILE)

    print('Walking complete, file count - ' + str(file_count))

    return result
