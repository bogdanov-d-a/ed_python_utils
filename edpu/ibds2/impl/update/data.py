from __future__ import annotations
from threading import Lock


def walk_data_with_mutex(path: str, mutex: Lock) -> dict[str, set[str]]:
    from ...utils.walkers import walk_data

    with mutex:
        return walk_data(path)


def update_data(root_def_path: str, root_data_path: str, root_data_path_recycle: str, data_sources: list[tuple[str, str]], data_mutex: Lock) -> None:
    from ...utils import mtime
    from concurrent.futures import ProcessPoolExecutor
    from typing import Optional

    with ProcessPoolExecutor(min(2 + len(data_sources), 4)) as executor:
        from ...utils.walkers import walk_def

        def_walk_future = executor.submit(walk_def, root_def_path)
        data_walk_future = executor.submit(walk_data_with_mutex, root_data_path, data_mutex)

        data_source_defs = list(executor.map(
            walk_def,
            list(map(
                lambda data_source: data_source[0],
                data_sources
            ))
        ))

        data_source_hash_to_location: dict[str, tuple[list[str], str]] = {}

        for data_source, data_source_def in zip(data_sources, data_source_defs):
            _, data_source_data_path = data_source

            for path_, data in data_source_def.files.items():
                hash_ = data.hash_

                if hash_ not in data_source_hash_to_location:
                    from ...utils.mappers.path_key import key_to_path
                    data_source_hash_to_location[hash_] = (key_to_path(path_), data_source_data_path)

        def_walk = def_walk_future.result()
        data_walk = data_walk_future.result()

    recycle_file_lists: dict[str, list[list[str]]] = {}
    empty_dirs: set[tuple] = set()

    getmtime_progress_printer = mtime.make_getmtime_progress_printer(root_data_path)
    setmtime_progress_printer = mtime.make_setmtime_progress_printer(root_data_path)

    def path_to_data_root(path: list[str]) -> str:
        from ...utils.path import path_to_root
        return path_to_root(path, root_data_path)

    def path_to_data_recycle_root(path: list[str]) -> str:
        from ...utils.path import path_to_root
        return path_to_root(path, root_data_path_recycle)

    def data_recycle_makedirs_helper(data_path: list[str]) -> None:
        from ...utils.file import makedirs_helper
        makedirs_helper(data_path, root_data_path_recycle, True)

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

    def copy_no_overwrite(src: str, dst: str) -> None:
        from os.path import exists
        from shutil import copy

        if exists(dst):
            raise Exception()

        print('Copying ' + src + ' to ' + dst)
        copy(src, dst)

    def copy_or_move_file(src: str, dst: str, move: bool) -> None:
        if not move:
            copy_no_overwrite(src, dst)
        else:
            from os import rename
            rename(src, dst)

    def move_for_recycling(path_: list[str]) -> None:
        from os import makedirs, rename

        makedirs(root_data_path_recycle, exist_ok=True)
        data_recycle_makedirs_helper(path_)
        rename(path_to_data_root(path_), path_to_data_recycle_root(path_))

    def action_create_dir(data_path: list[str]) -> None:
        from ...utils.file import makedirs_helper
        makedirs_helper(data_path, root_data_path, False)

    def action_recycle_file(data_path: list[str]) -> None:
        from ...utils.file import hash_file

        data_path_abs = path_to_data_root(data_path)
        hash_ = hash_file(data_path_abs)

        if hash_ not in recycle_file_lists:
            recycle_file_lists[hash_] = []

        recycle_file_lists[hash_].append(data_path)

    def action_create_file(data_path: list[str]) -> None:
        from ...utils.mappers.path_key import path_to_key

        def_walk_data = def_walk.files[path_to_key(data_path)]
        find_file_by_hash_result = find_file_by_hash(def_walk_data.hash_)

        if find_file_by_hash_result is None:
            print('File not found, hash ' + def_walk_data.hash_)
            return

        data_path_abs = path_to_data_root(data_path)
        copy_or_move_file(find_file_by_hash_result.path_, data_path_abs, find_file_by_hash_result.can_move)
        mtime.setmtime(data_path_abs, def_walk_data.mtime, setmtime_progress_printer)

    def action_update_file(data_path: list[str]) -> None:
        from ...utils.mappers.path_key import path_to_key

        data_path_abs = path_to_data_root(data_path)
        def_walk_data = def_walk.files[path_to_key(data_path)]

        if def_walk_data.mtime != mtime.getmtime(data_path_abs, getmtime_progress_printer):
            from ...utils.file import hash_file

            if hash_file(data_path_abs) != def_walk_data.hash_:
                find_file_by_hash_result = find_file_by_hash(def_walk_data.hash_)

                if find_file_by_hash_result is None:
                    print('File not found, hash ' + def_walk_data.hash_)
                    return

                move_for_recycling(data_path)
                copy_or_move_file(find_file_by_hash_result.path_, data_path_abs, find_file_by_hash_result.can_move)

            mtime.setmtime(data_path_abs, def_walk_data.mtime, setmtime_progress_printer)

    def action_remove_empty_dir(data_path: list[str]) -> None:
        empty_dirs.add(tuple(data_path))

    def remove_empty_dir() -> bool:
        for empty_dir in list(empty_dirs):
            try:
                from os import rmdir

                rmdir(path_to_data_root(list(empty_dir)))
                empty_dirs.remove(empty_dir)

                return True
            except:
                pass

        return False

    with data_mutex:
        from ...utils.utils import intersection_handler
        from edpu.file_tree_walker import TYPE_DIR, TYPE_FILE

        intersection_handler(def_walk.dirs, data_walk[TYPE_DIR], False, action_create_dir)

        def_walk_file_keys = set(def_walk.files.keys())

        intersection_handler(data_walk[TYPE_FILE], def_walk_file_keys, False, action_recycle_file)
        intersection_handler(def_walk_file_keys, data_walk[TYPE_FILE], False, action_create_file)
        intersection_handler(def_walk_file_keys, data_walk[TYPE_FILE], True, action_update_file)

        for recycle_files in recycle_file_lists.values():
            for recycle_file in recycle_files:
                move_for_recycling(recycle_file)

        intersection_handler(data_walk[TYPE_DIR], def_walk.dirs, False, action_remove_empty_dir)

        while len(empty_dirs) > 0:
            if not remove_empty_dir():
                raise Exception()
