from __future__ import annotations
from ...utils import time


def update_data(root_def_path: str, root_data_path: str, root_data_path_recycle: str, data_sources: list[tuple[str, str]], skip_descript_ion: bool, collector: time.Collector) -> None:
    from ....file_tree_walker import TYPE_DIR, TYPE_FILE
    from ...utils.walkers import WalkDefResult
    from concurrent.futures import ProcessPoolExecutor

    def get_data_source_defs(executor: ProcessPoolExecutor) -> list[WalkDefResult]:
        from ...utils.walk_helpers import walk_def
        from operator import itemgetter

        data_source_def_tuples = list(executor.map(
            walk_def,
            list(map(
                itemgetter(0),
                data_sources
            ))
        ))

        for data_source_collector in map(itemgetter(1), data_source_def_tuples):
            collector.merge(data_source_collector)

        return list(map(itemgetter(0), data_source_def_tuples))

    def get_data_source_hash_to_location(executor: ProcessPoolExecutor) -> dict[str, tuple[list[str], str]]:
        result: dict[str, tuple[list[str], str]] = {}

        for data_source, data_source_def in zip(data_sources, get_data_source_defs(executor)):
            _, data_source_data_path = data_source

            for path_, data in data_source_def.files.items():
                hash_ = data.hash_

                if hash_ not in result:
                    from ...utils.mappers.path_key import key_to_path
                    result[hash_] = (key_to_path(path_), data_source_data_path)

        return result

    def load_data():
        from ...utils.mp_global import make_process_pool_executor

        with make_process_pool_executor(min(2 + len(data_sources), 4)) as executor:
            from ...utils.walk_helpers import walk_def, walk_data

            def_walk_future = executor.submit(walk_def, root_def_path)
            data_walk_future = executor.submit(walk_data, root_data_path, skip_descript_ion)

            data_source_hash_to_location = get_data_source_hash_to_location(executor)

            def_walk, def_collector = def_walk_future.result()
            data_walk, data_collector = data_walk_future.result()

            collector.merge(def_collector).merge(data_collector)

        return (def_walk, data_walk, data_source_hash_to_location)

    def path_to_data_root(path: list[str]) -> str:
        from ...utils.path import path_to_root
        return path_to_root(path, root_data_path)

    def path_to_data_recycle_root(path: list[str]) -> str:
        from ...utils.path import path_to_root
        return path_to_root(path, root_data_path_recycle)

    def data_recycle_makedirs_helper(data_path: list[str]) -> None:
        from ...utils.file import makedirs_helper
        from os import makedirs

        makedirs(root_data_path_recycle, exist_ok=True)
        makedirs_helper(data_path, root_data_path_recycle, TYPE_FILE)

    def copy_no_overwrite(src: str, dst: str) -> None:
        from ...utils.file import copy_no_overwrite as impl
        impl(src, dst, True, time.get_perf_counter_measure(collector, time.Key.WORKER1_COPY_FILE))

    def copy_or_move_file(src: str, dst: str, move: bool) -> None:
        if not move:
            copy_no_overwrite(src, dst)
        else:
            from os import rename
            rename(src, dst)

    def move_to_recycle(path_: list[str]) -> None:
        from os import rename

        data_recycle_makedirs_helper(path_)
        rename(path_to_data_root(path_), path_to_data_recycle_root(path_))

    def print_file_not_found(hash: str) -> None:
        from ...utils.mp_global import print_lock

        with print_lock():
            print(f'File not found, hash {hash}')

    def main() -> None:
        from ...utils import mtime
        from ...utils.mp_global import data_lock
        from ...utils.utils import intersection, IntersectionType
        from typing import Optional

        def_walk, data_walk, data_source_hash_to_location = load_data()
        def_walk_file_keys = set(def_walk.files.keys())

        recycle_file_lists: dict[str, list[list[str]]] = {}

        getmtime_progress_printer = mtime.make_getmtime_progress_printer(root_data_path)
        setmtime_progress_printer = mtime.make_setmtime_progress_printer(root_data_path)

        class FindFileByHashResult:
            def __init__(self: FindFileByHashResult, path_: str, can_move: bool) -> None:
                self.path_ = path_
                self.can_move = can_move

        def find_file_by_hash(hash_: str) -> Optional[FindFileByHashResult]:
            recycle_files = recycle_file_lists.get(hash_)

            if recycle_files is not None and len(recycle_files) > 0:
                recycle_file = recycle_files[0]
                recycle_file_lists[hash_] = recycle_files[1:]
                return FindFileByHashResult(path_to_data_root(recycle_file), True)

            data_source_location = data_source_hash_to_location.get(hash_)

            if data_source_location is not None:
                from ...utils.path import path_to_root
                return FindFileByHashResult(path_to_root(data_source_location[0], data_source_location[1]), False)

            return None

        def create_missing_dirs() -> None:
            for data_path in intersection(def_walk.dirs, data_walk[TYPE_DIR], IntersectionType.DIFFERENT):
                from ...utils.file import makedirs_helper
                makedirs_helper(data_path, root_data_path, TYPE_DIR)

        def mark_odd_files_for_recycling() -> None:
            for data_path in intersection(data_walk[TYPE_FILE], def_walk_file_keys, IntersectionType.DIFFERENT):
                from ...utils.file import hash_file

                data_path_abs = path_to_data_root(data_path)
                hash_ = hash_file(data_path_abs, collector)

                if hash_ not in recycle_file_lists:
                    recycle_file_lists[hash_] = []

                recycle_file_lists[hash_].append(data_path)

        def create_missing_files() -> None:
            for data_path in intersection(def_walk_file_keys, data_walk[TYPE_FILE], IntersectionType.DIFFERENT):
                from ...utils.mappers.path_key import path_to_key

                def_walk_data = def_walk.files[path_to_key(data_path)]
                find_file_by_hash_result = find_file_by_hash(def_walk_data.hash_)

                if find_file_by_hash_result is None:
                    print_file_not_found(def_walk_data.hash_)
                    continue

                data_path_abs = path_to_data_root(data_path)
                copy_or_move_file(find_file_by_hash_result.path_, data_path_abs, find_file_by_hash_result.can_move)
                mtime.setmtime(data_path_abs, def_walk_data.mtime, setmtime_progress_printer, collector)

        def update_files() -> None:
            for data_path in intersection(def_walk_file_keys, data_walk[TYPE_FILE], IntersectionType.MATCHING):
                from ...utils.mappers.path_key import path_to_key

                data_path_abs = path_to_data_root(data_path)
                def_walk_data = def_walk.files[path_to_key(data_path)]

                if def_walk_data.mtime != mtime.getmtime(data_path_abs, getmtime_progress_printer, collector):
                    from ...utils.file import hash_file

                    if hash_file(data_path_abs, collector) != def_walk_data.hash_:
                        find_file_by_hash_result = find_file_by_hash(def_walk_data.hash_)

                        if find_file_by_hash_result is None:
                            print_file_not_found(def_walk_data.hash_)
                            continue

                        move_to_recycle(data_path)
                        copy_or_move_file(find_file_by_hash_result.path_, data_path_abs, find_file_by_hash_result.can_move)

                    mtime.setmtime(data_path_abs, def_walk_data.mtime, setmtime_progress_printer, collector)

        def move_marked_files_to_recycle() -> None:
            for recycle_files in recycle_file_lists.values():
                for recycle_file in recycle_files:
                    move_to_recycle(recycle_file)

        def remove_odd_dirs() -> None:
            set_: set[str] = set()

            def fill_set() -> None:
                for data_path in intersection(data_walk[TYPE_DIR], def_walk.dirs, IntersectionType.DIFFERENT):
                    from ...utils.mappers.path_key import path_to_key
                    set_.add(path_to_key(data_path))

            def remove() -> None:
                def remove_one() -> bool:
                    for empty_dir in set_:
                        try:
                            from ...utils.mappers.path_key import key_to_path
                            from os import rmdir

                            rmdir(path_to_data_root(key_to_path(empty_dir)))
                            set_.remove(empty_dir)

                            return True
                        except:
                            pass

                    return False

                while len(set_) > 0:
                    if not remove_one():
                        raise Exception()

            fill_set()
            remove()

        with data_lock():
            create_missing_dirs()
            mark_odd_files_for_recycling()
            create_missing_files()
            update_files()
            move_marked_files_to_recycle()
            remove_odd_dirs()

    main()
