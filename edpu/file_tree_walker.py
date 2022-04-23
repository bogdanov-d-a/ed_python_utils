import os


TYPE_DIR = 'dir'
TYPE_FILE = 'file'


def walk(root_path, ignore_callback=lambda *_: False):
    if not os.path.isdir(root_path):
        raise Exception(root_path + ' does not exist')

    result = { TYPE_DIR: [], TYPE_FILE: [] }

    for cur_root_path, dirs, files in os.walk(root_path):
        rel_path_text = os.path.relpath(cur_root_path, root_path)
        if rel_path_text == '.':
            rel_path = []
        else:
            rel_path = rel_path_text.split(os.sep)

        def handler(elems, type):
            for elem in elems:
                if not ignore_callback(type, rel_path + [elem]):
                    result[type].append(rel_path + [elem])

        handler(dirs, TYPE_DIR)
        handler(files, TYPE_FILE)

    return result
