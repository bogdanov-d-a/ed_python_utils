from __future__ import annotations
from typing import Callable
from edpu.file_tree_walker import walk, TYPE_DIR, TYPE_FILE
from .utils import utils
from .def_file import DefFileData, load_def_file
from .mappers.path_key import path_to_key


def make_file_progress_printer(period: float, annotation: str, path_: str) -> Callable[[int], None]:
    from edpu.throttling import TimeBasedAggregator
    return TimeBasedAggregator.make_number_sum_printer(period, f'walkers.{annotation} {path_}')


def walk_data(data_path: str) -> dict[str, set[str]]:
    data_walk = walk(data_path, file_progress=make_file_progress_printer(0.5, 'walk_data', data_path))
    result: dict[str, set[str]] = { TYPE_DIR: set(), TYPE_FILE: set() }

    for dir_path in data_walk[TYPE_DIR]:
        dir_path_key = path_to_key(dir_path)
        result[TYPE_DIR].add(dir_path_key)

    for file_path in data_walk[TYPE_FILE]:
        file_path_key = path_to_key(file_path)
        result[TYPE_FILE].add(file_path_key)

    return result


WalkDefDirs = set[str]
WalkDefFiles = dict[str, DefFileData]

class WalkDefResult:
    def __init__(self: WalkDefResult, dirs: WalkDefDirs, files: WalkDefFiles) -> None:
        self.dirs = dirs
        self.files = files

    def __eq__(self: WalkDefResult, other: WalkDefResult) -> bool:
        if isinstance(other, self.__class__):
            return self.dirs == other.dirs and self.files == other.files
        return False


def walk_def(def_path: str) -> WalkDefResult:
    def_walk = walk(def_path, lambda type_, _: type_ == TYPE_DIR, make_file_progress_printer(0.1, 'walk_def', def_path))[TYPE_FILE]

    result_dirs: WalkDefDirs = set()
    result_files: WalkDefFiles = {}

    for def_file_path in def_walk:
        type_, data_path = utils.def_path_to_data_path(def_file_path)
        data_path_key = path_to_key(data_path)

        if type_ == TYPE_FILE:
            abs_def_file_path = utils.path_to_root(def_file_path, def_path)
            result_files[data_path_key] = load_def_file(abs_def_file_path)
        else:
            result_dirs.add(data_path_key)

    return WalkDefResult(result_dirs, result_files)
