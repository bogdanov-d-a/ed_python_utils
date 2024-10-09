from .. import storage_finder
from ..string_utils import merge_with_space, quotation_mark_wrap
from .user_data import COLLECTION_VALUE_LOCATIONS, CollectionDict, CollectionList, COLLECTION_VALUE_DUPLICATE_SKIP_PATHS
from . import collection_definition
from . import ibds_utils
from . import file_tree_snapshot
from . import path_generator
from . import storage_device


def _collection_common(data_dir: str, collection_name: str, collection_path: str, skip_paths: list[str]) -> None:
    data = collection_definition.load_common_data(path_generator.gen_common_file_path(collection_name, data_dir))
    table: dict[str, list[str]] = {}

    for path, hash_ in data:
        if ibds_utils.path_needs_skip(path.split(file_tree_snapshot.INDEX_PATH_SEPARATOR), skip_paths):
            continue
        if hash_ not in table:
            table[hash_] = []
        table[hash_].append(path)

    table_items: list[tuple[str, list[str]]] = ibds_utils.key_sorted_dict_items(table)

    for hash_, paths in table_items:
        if (len(paths) > 1):
            print(f'REM {hash_}')

            for path in paths:
                from os.path import join

                print(merge_with_space([
                    'REM',
                    'del',
                    '/f',
                    '/q',
                    quotation_mark_wrap(join(collection_path, path)),
                ]))

            print()


def _collection_storage_device(data_dir: str, collection_name: str, storage_device_: storage_device.StorageDevice) -> None:
    data = file_tree_snapshot.load_index(path_generator.gen_index_file_path(collection_name, storage_device_, data_dir))
    table: dict[str, list[str]] = {}

    for path, info in data.getPairList():
        if info.getHash() not in table:
            table[info.getHash()] = []
        table[info.getHash()].append(path)

    table_items: list[tuple[str, list[str]]] = ibds_utils.key_sorted_dict_items(table)
    for hash_, paths in table_items:
        if (len(paths) > 1):
            print(hash_ + ' ' + str(paths))


def collections_common(data_dir: str, storage_device_: storage_device.StorageDevice, collection_dict: CollectionDict) -> None:
    path_prefix = storage_finder.keep_getting_storage_path(storage_device_.getName()) if storage_device_.isRemovable() else ''

    collection_dict_items: CollectionList = ibds_utils.key_sorted_dict_items(collection_dict)

    for collection_name, data in collection_dict_items:
        for location in data[COLLECTION_VALUE_LOCATIONS]:
            if location.getStorageDevice().getName() == storage_device_.getName():
                _collection_common(data_dir, collection_name, path_prefix + location.getPath(), data[COLLECTION_VALUE_DUPLICATE_SKIP_PATHS])
