from threading import Lock
from typing import Callable
from .walkers import walk_def, walk_data
from .def_file import save_def_file
from . import utils
from .constants import *
from concurrent.futures import ProcessPoolExecutor
import os


def walk_data_with_mutex(path: str, mutex: Lock) -> dict[str, set[str]]:
    with mutex:
        return walk_data(path)


def update_definition(root_data_path: str, root_def_path: str, skip_mtime: bool, data_mutex: Lock) -> None:
    with ProcessPoolExecutor(2) as executor:
        data_walk_future = executor.submit(walk_data_with_mutex, root_data_path, data_mutex)
        def_walk_future = executor.submit(walk_def, root_def_path)

        data_walk = data_walk_future.result()
        def_walk = def_walk_future.result()

    getmtime_progress_printer = utils.make_getmtime_progress_printer(root_data_path)

    def path_to_def_root(path: list[str]) -> str:
        return utils.path_to_root(path, root_def_path)

    def path_to_data_root(path: list[str]) -> str:
        return utils.path_to_root(path, root_data_path)

    def def_makedirs_helper(def_path: list[str]) -> None:
        utils.makedirs_helper(def_path, root_def_path, True)

    def debug_remove(path: str) -> None:
        if utils.debug:
            print('debug_remove ' + path)
        else:
            os.remove(path)

    def action_remove(_, def_path: list[str]) -> None:
        debug_remove(path_to_def_root(def_path))

    def action_create_dir(_, def_path: list[str]) -> None:
        def_makedirs_helper(def_path)
        open(path_to_def_root(def_path), 'w')

    def action_create_file(data_path: list[str], def_path: list[str]) -> None:
        data_path_abs = path_to_data_root(data_path)
        def_makedirs_helper(def_path)
        save_def_file(path_to_def_root(def_path), utils.hash_file(data_path_abs), utils.getmtime(data_path_abs, getmtime_progress_printer))

    def action_update_file(data_path: list[str], def_path: list[str]) -> None:
        if skip_mtime:
            return

        def_data = def_walk[TYPE_FILE][utils.path_to_key(data_path)]
        data_path_abs = path_to_data_root(data_path)
        actual_mtime = utils.getmtime(data_path_abs, getmtime_progress_printer)

        if def_data[MTIME_KEY] != actual_mtime:
            save_def_file(path_to_def_root(def_path), utils.hash_file(data_path_abs), actual_mtime)

    def intersection_handler_with_def_path(content_type: str, main_list, aux_list, use_intersection: bool, action: Callable[[list[str], list[str]], None]):
        utils.intersection_handler(content_type, main_list, aux_list, use_intersection, lambda data_path: action(data_path, utils.data_path_to_def_path(data_path, content_type)))

    with data_mutex:
        intersection_handler_with_def_path(TYPE_DIR, def_walk, data_walk, False, action_remove)
        intersection_handler_with_def_path(TYPE_DIR, data_walk, def_walk, False, action_create_dir)

        intersection_handler_with_def_path(TYPE_FILE, def_walk, data_walk, False, action_remove)
        intersection_handler_with_def_path(TYPE_FILE, data_walk, def_walk, False, action_create_file)
        intersection_handler_with_def_path(TYPE_FILE, data_walk, def_walk, True, action_update_file)
