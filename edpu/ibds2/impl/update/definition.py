from threading import Lock


def walk_data_with_mutex(path: str, mutex: Lock) -> dict[str, set[str]]:
    from ...utils.walkers import walk_data

    with mutex:
        return walk_data(path)


def update_definition(root_data_path: str, root_def_path: str, skip_mtime: bool, debug: bool, data_mutex: Lock) -> None:
    from ...utils import mtime
    from concurrent.futures import ProcessPoolExecutor
    from typing import Callable

    with ProcessPoolExecutor(2) as executor:
        from ...utils.walkers import walk_def

        data_walk_future = executor.submit(walk_data_with_mutex, root_data_path, data_mutex)
        def_walk_future = executor.submit(walk_def, root_def_path)

        data_walk = data_walk_future.result()
        def_walk = def_walk_future.result()

    getmtime_progress_printer = mtime.make_getmtime_progress_printer(root_data_path)

    def path_to_def_root(path: list[str]) -> str:
        from ...utils.path import path_to_root
        return path_to_root(path, root_def_path)

    def path_to_data_root(path: list[str]) -> str:
        from ...utils.path import path_to_root
        return path_to_root(path, root_data_path)

    def def_makedirs_helper(def_path: list[str]) -> None:
        from ...utils.file import makedirs_helper
        makedirs_helper(def_path, root_def_path, True)

    def debug_remove(path: str) -> None:
        if debug:
            print('debug_remove ' + path)
        else:
            from os import remove
            remove(path)

    def action_remove(_, def_path: list[str]) -> None:
        debug_remove(path_to_def_root(def_path))

    def action_create_dir(_, def_path: list[str]) -> None:
        def_makedirs_helper(def_path)
        open(path_to_def_root(def_path), 'w')

    def action_create_file(data_path: list[str], def_path: list[str]) -> None:
        from ...utils.def_file import DefFile
        from ...utils.file import hash_file

        data_path_abs = path_to_data_root(data_path)
        def_makedirs_helper(def_path)
        DefFile(hash_file(data_path_abs), mtime.getmtime(data_path_abs, getmtime_progress_printer)).save(path_to_def_root(def_path))

    def action_update_file(data_path: list[str], def_path: list[str]) -> None:
        from ...utils.mappers.path_key import path_to_key

        if skip_mtime:
            return

        def_data = def_walk.files[path_to_key(data_path)]
        data_path_abs = path_to_data_root(data_path)
        actual_mtime = mtime.getmtime(data_path_abs, getmtime_progress_printer)

        if def_data.mtime != actual_mtime:
            from ...utils.def_file import DefFile
            from ...utils.file import hash_file

            DefFile(hash_file(data_path_abs), actual_mtime).save(path_to_def_root(def_path))

    def intersection_handler_with_def_path(content_type: str, main_list: set[str], aux_list: set[str], use_intersection: bool, action: Callable[[list[str], list[str]], None]):
        from ...utils.mappers.def_data_path import data_path_to_def_path
        from ...utils.utils import intersection_handler

        intersection_handler(main_list, aux_list, use_intersection, lambda data_path: action(data_path, data_path_to_def_path(data_path, content_type)))

    with data_mutex:
        from edpu.file_tree_walker import TYPE_DIR, TYPE_FILE

        intersection_handler_with_def_path(TYPE_DIR, def_walk.dirs, data_walk[TYPE_DIR], False, action_remove)
        intersection_handler_with_def_path(TYPE_DIR, data_walk[TYPE_DIR], def_walk.dirs, False, action_create_dir)

        def_walk_file_keys = set(def_walk.files.keys())

        intersection_handler_with_def_path(TYPE_FILE, def_walk_file_keys, data_walk[TYPE_FILE], False, action_remove)
        intersection_handler_with_def_path(TYPE_FILE, data_walk[TYPE_FILE], def_walk_file_keys, False, action_create_file)
        intersection_handler_with_def_path(TYPE_FILE, data_walk[TYPE_FILE], def_walk_file_keys, True, action_update_file)
