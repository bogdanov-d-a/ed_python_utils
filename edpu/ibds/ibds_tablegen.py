from typing import Optional
from . import file_tree_snapshot
from . import ibds_utils


def indexes(index_list: list[file_tree_snapshot.Index]) -> dict[str, list[Optional[file_tree_snapshot.FileInfo]]]:
    table: dict[str, list[Optional[file_tree_snapshot.FileInfo]]] = {}

    paths: set[str] = set()
    for index_main in index_list:
        paths |= index_main.getKeySet()

    for path in paths:
        table[path] = [None] * len(index_list)

    for path in table.keys():
        for index_index in range(len(index_list)):
            index = index_list[index_index]
            if index.hasData(path):
                table[path][index_index] = index.getData(path)

    return table


def index_files(index_file_list: list[str]) -> dict[str, list[Optional[file_tree_snapshot.FileInfo]]]:
    index_list = list(map(lambda path: file_tree_snapshot.load_index(path), index_file_list))
    return indexes(index_list)


def indexes_by_hash(index_list: list[file_tree_snapshot.Index]) -> dict[str, list[bool]]:
    table: dict[str, list[bool]] = {}

    hashes: list[set[str]] = []
    for index_main in index_list:
        hashes_main: set[str] = set()
        for _, fileInfo in index_main.getPairList():
            hashes_main.add(fileInfo.getHash())
        hashes.append(hashes_main)

    hashes_all: set[str] = set()
    for hashes_main in hashes:
        hashes_all |= hashes_main

    for hash_ in hashes_all:
        table[hash_] = [False] * len(index_list)

    for hash_ in table.keys():
        for index_index in range(len(index_list)):
            if hash_ in hashes[index_index]:
                table[hash_][index_index] = True

    return table


def _get_data_hashes(data: list[Optional[file_tree_snapshot.FileInfo]], keep_none: bool=False) -> list[Optional[str]]:
    return list(map(lambda x: x.getHash() if x is not None else None, filter(lambda x: keep_none or x is not None, data)))


def get_data_hashes(data: list[Optional[file_tree_snapshot.FileInfo]]) -> list[str]:
    return _get_data_hashes(data)


def get_data_hashes_with_none(data: list[Optional[file_tree_snapshot.FileInfo]]) -> list[Optional[str]]:
    return _get_data_hashes(data, True)


def get_same_hash(data: list[Optional[file_tree_snapshot.FileInfo]]) -> Optional[str]:
    hashes = get_data_hashes(data)
    return hashes[0] if ibds_utils.is_same_list(hashes) else None
