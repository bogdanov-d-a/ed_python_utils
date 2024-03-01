from __future__ import annotations
import os
import codecs
from edpu import file_hashing
from . import file_tree_scanner
from . import ibds_utils


INDEX_PATH_SEPARATOR = '\\'


class FileInfo:
    def __init__(self: FileInfo, mtime: float, hash_: str) -> None:
        self.setMtime(mtime)
        self.setHash(hash_)

    def getMtime(self: FileInfo) -> float:
        return self._mtime

    def setMtime(self: FileInfo, mtime: float) -> None:
        self._mtime = mtime

    def getHash(self: FileInfo) -> str:
        return self._hash

    def setHash(self: FileInfo, hash_: str) -> None:
        self._hash = hash_


class Index:
    def __init__(self: Index) -> None:
        self._data: dict[str, FileInfo] = {}

    def addData(self: Index, path: str, fileInfo: FileInfo) -> None:
        self._data[path] = fileInfo

    def hasData(self: Index, path: str) -> bool:
        return path in self._data

    def getData(self: Index, path: str) -> FileInfo:
        return self._data[path]

    def getPairList(self: Index) -> list[tuple[str, FileInfo]]:
        return ibds_utils.key_sorted_dict_items(self._data)

    def getKeySet(self: Index) -> set[str]:
        return set(self._data.keys())


def _create_index(tree_path: str, skip_paths: list[str]) -> Index:
    index = Index()

    for rel_path in file_tree_scanner.scan(tree_path, skip_paths):
        rel_path_key = INDEX_PATH_SEPARATOR.join(rel_path)
        abs_path = os.path.join(tree_path, os.sep.join(rel_path))
        print('Calculating hash for ' + rel_path_key)
        index.addData(INDEX_PATH_SEPARATOR.join(rel_path), FileInfo(os.path.getmtime(abs_path), file_hashing.sha1_file(abs_path)))

    return index


def _update_index(old_index: Index, tree_path: str, skip_paths: list[str], skip_mtime: bool) -> Index:
    index = Index()

    for rel_path in file_tree_scanner.scan(tree_path, skip_paths):
        abs_path = os.path.join(tree_path, os.sep.join(rel_path))

        mdate: float = 0
        if not skip_mtime:
            mdate = os.path.getmtime(abs_path)

        rel_path_key = INDEX_PATH_SEPARATOR.join(rel_path)

        if old_index.hasData(rel_path_key) and (skip_mtime or old_index.getData(rel_path_key).getMtime() == mdate):
            hash_ = old_index.getData(rel_path_key).getHash()
            if skip_mtime:
                mdate = old_index.getData(rel_path_key).getMtime()
        else:
            print('Calculating hash for ' + rel_path_key)
            hash_ = file_hashing.sha1_file(abs_path)
            if skip_mtime:
                mdate = os.path.getmtime(abs_path)

        index.addData(rel_path_key, FileInfo(mdate, hash_))

    return index


def load_index(file_path: str) -> Index:
    with codecs.open(file_path, 'r', 'utf-8-sig') as input_:
        data_ = Index()

        for line in input_.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            parts = line.split(' ', 2)
            if len(parts) != 3:
                raise Exception('load_index bad format')
            data_.addData(parts[2], FileInfo(float(parts[0]), parts[1]))

        return data_


def save_index(index: Index, file_path: str) -> None:
    with codecs.open(file_path, 'w', 'utf-8-sig') as output:
        for path, data in index.getPairList():
            output.write(str(data.getMtime()))
            output.write(' ')
            output.write(data.getHash())
            output.write(' ')
            output.write(path)
            output.write('\n')


def update_index_file(tree_path: str, index_path: str, skip_paths: list[str], skip_mtime: bool) -> None:
    if os.path.isfile(index_path):
        old_index = load_index(index_path)
        new_index = _update_index(old_index, tree_path, skip_paths, skip_mtime)
    else:
        new_index = _create_index(tree_path, skip_paths)
    save_index(new_index, index_path)
