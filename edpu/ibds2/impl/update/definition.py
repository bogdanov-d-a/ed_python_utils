from ...utils import time
from threading import Lock


def update_definition(root_data_path: str, root_def_path: str, skip_mtime: bool, debug: bool, data_mutex: Lock, collector: time.Collector) -> None:
    from ...utils import mtime
    from ...utils.utils import IntersectionType
    from concurrent.futures import ProcessPoolExecutor
    from typing import Iterator

    with ProcessPoolExecutor(2) as executor:
        from ...utils.walk_helpers import walk_def, walk_data

        data_walk_future = executor.submit(walk_data, root_data_path, data_mutex)
        def_walk_future = executor.submit(walk_def, root_def_path)

        data_walk, data_collector = data_walk_future.result()
        def_walk, def_collector = def_walk_future.result()

        collector.merge(data_collector).merge(def_collector)

    getmtime_progress_printer = mtime.make_getmtime_progress_printer(root_data_path)

    def path_to_def_root(path: list[str]) -> str:
        from ...utils.path import path_to_root
        return path_to_root(path, root_def_path)

    def path_to_data_root(path: list[str]) -> str:
        from ...utils.path import path_to_root
        return path_to_root(path, root_data_path)

    def def_makedirs_helper(def_path: list[str]) -> None:
        from ...utils.file import makedirs_helper
        makedirs_helper(def_path, root_def_path, TYPE_FILE)

    def debug_remove(path: str) -> None:
        if debug:
            print('debug_remove ' + path)
        else:
            from os import remove
            remove(path)

    def intersection_with_def_path(content_type: str, main_list: set[str], aux_list: set[str], type: IntersectionType) -> Iterator[tuple[list[str], list[str]]]:
        from ...utils.mappers.def_data_path import data_path_to_def_path
        from ...utils.utils import intersection

        for data_path in intersection(main_list, aux_list, type):
            yield (data_path, data_path_to_def_path(data_path, content_type))

    with data_mutex:
        from edpu.file_tree_walker import TYPE_DIR, TYPE_FILE

        for _, def_path in intersection_with_def_path(TYPE_DIR, def_walk.dirs, data_walk[TYPE_DIR], IntersectionType.DIFFERENT):
            debug_remove(path_to_def_root(def_path))

        for _, def_path in intersection_with_def_path(TYPE_DIR, data_walk[TYPE_DIR], def_walk.dirs, IntersectionType.DIFFERENT):
            def_makedirs_helper(def_path)
            open(path_to_def_root(def_path), 'w').close()

        def_walk_file_keys = set(def_walk.files.keys())

        for _, def_path in intersection_with_def_path(TYPE_FILE, def_walk_file_keys, data_walk[TYPE_FILE], IntersectionType.DIFFERENT):
            debug_remove(path_to_def_root(def_path))

        for data_path, def_path in intersection_with_def_path(TYPE_FILE, data_walk[TYPE_FILE], def_walk_file_keys, IntersectionType.DIFFERENT):
            from ...utils.def_file import DefFile
            from ...utils.file import hash_file

            data_path_abs = path_to_data_root(data_path)
            def_makedirs_helper(def_path)
            DefFile(hash_file(data_path_abs), mtime.getmtime(data_path_abs, getmtime_progress_printer, collector)).save(path_to_def_root(def_path))

        for data_path, def_path in intersection_with_def_path(TYPE_FILE, data_walk[TYPE_FILE], def_walk_file_keys, IntersectionType.MATCHING):
            from ...utils.mappers.path_key import path_to_key

            if skip_mtime:
                continue

            def_data = def_walk.files[path_to_key(data_path)]
            data_path_abs = path_to_data_root(data_path)
            actual_mtime = mtime.getmtime(data_path_abs, getmtime_progress_printer, collector)

            if def_data.mtime != actual_mtime:
                from ...utils.def_file import DefFile
                from ...utils.file import hash_file

                DefFile(hash_file(data_path_abs), actual_mtime).save(path_to_def_root(def_path))
