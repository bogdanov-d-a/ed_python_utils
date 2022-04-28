from edpu import file_tree_walker
from .constants import *
from .utils import *
from .def_file import load_def_file


def walk_data(data_path):
    data_walk = file_tree_walker.walk(data_path)
    result = { TYPE_DIR: set(), TYPE_FILE: {} }

    for dir_path in data_walk.get(TYPE_DIR):
        dir_path_key = path_to_key(dir_path)
        result.get(TYPE_DIR).add(dir_path_key)

    for file_path in data_walk.get(TYPE_FILE):
        file_path_key = path_to_key(file_path)
        abs_file_path = path_to_root(file_path, data_path)
        result.get(TYPE_FILE)[file_path_key] = getmtime(abs_file_path)

    return result


def walk_def(def_path):
    def_walk = file_tree_walker.walk(def_path, lambda type_, _: type_ == TYPE_DIR).get(TYPE_FILE)
    result = { TYPE_DIR: set(), TYPE_FILE: {} }

    for def_file_path in def_walk:
        type_, data_path = def_path_to_data_path(def_file_path)
        data_path_key = path_to_key(data_path)

        if type_ == TYPE_FILE:
            abs_def_file_path = path_to_root(def_file_path, def_path)
            def_file_data = load_def_file(abs_def_file_path)
            result.get(TYPE_FILE)[data_path_key] = {
                HASH_KEY: def_file_data.get(HASH_KEY),
                MTIME_KEY: def_file_data.get(MTIME_KEY),
            }
        else:
            result.get(TYPE_DIR).add(data_path_key)

    return result
