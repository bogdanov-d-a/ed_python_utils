from typing import Callable
from edpu import file_tree_walker
from .constants import *
from . import utils
from .def_file import load_def_file


def make_file_progress_printer(period: float, annotation: str, path_: str) -> Callable[[int], None]:
    from edpu.throttling import TimeBasedAggregator
    return TimeBasedAggregator.make_number_sum_printer(period, f'walkers.{annotation} {path_}')


def walk_data(data_path: str) -> dict[str, set[str]]:
    data_walk = file_tree_walker.walk(data_path, file_progress=make_file_progress_printer(0.5, 'walk_data', data_path))
    result: dict[str, set[str]] = { TYPE_DIR: set(), TYPE_FILE: set() }

    for dir_path in data_walk[TYPE_DIR]:
        dir_path_key = utils.path_to_key(dir_path)
        result[TYPE_DIR].add(dir_path_key)

    for file_path in data_walk[TYPE_FILE]:
        file_path_key = utils.path_to_key(file_path)
        result[TYPE_FILE].add(file_path_key)

    return result


def walk_def(def_path: str) -> dict[str, Any]:
    def_walk = file_tree_walker.walk(def_path, lambda type_, _: type_ == TYPE_DIR, make_file_progress_printer(0.1, 'walk_def', def_path))[TYPE_FILE]
    result: dict[str, Any] = { TYPE_DIR: set(), TYPE_FILE: {} }

    for def_file_path in def_walk:
        type_, data_path = utils.def_path_to_data_path(def_file_path)
        data_path_key = utils.path_to_key(data_path)

        if type_ == TYPE_FILE:
            abs_def_file_path = utils.path_to_root(def_file_path, def_path)
            result[TYPE_FILE][data_path_key] = load_def_file(abs_def_file_path)
        else:
            result[TYPE_DIR].add(data_path_key)

    return result
