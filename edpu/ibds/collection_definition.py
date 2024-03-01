import codecs
from typing import Optional
from . import file_tree_snapshot
from .user_data import CollectionDict, COLLECTION_VALUE_LOCATIONS
from . import ibds_utils
from . import collection_tablegen
from . import ibds_tablegen
from . import path_generator


def save_common_data(common_data: list[tuple[str, str]], file_path: str) -> None:
    with codecs.open(file_path, 'w', 'utf-8-sig') as output:
        for path, hash_ in common_data:
            output.write(hash_)
            output.write(' ')
            output.write(path)
            output.write('\n')


def load_common_data(file_path: str) -> list[tuple[str, str]]:
    with codecs.open(file_path, 'r', 'utf-8-sig') as input_:
        data_: list[tuple[str, str]] = []

        for line in input_.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            parts = line.split(' ', 1)
            if len(parts) != 2:
                raise Exception('load_common_data bad format')
            data_.append((parts[1], parts[0]))

        return data_


def save_hashset_data(hashset_data: set[str], file_path: str) -> None:
    with codecs.open(file_path, 'w', 'utf-8-sig') as output:
        for hash_ in sorted(list(hashset_data)):
            output.write(hash_)
            output.write('\n')


def _generate_collection_definition(data_dir: str, collection_dict: CollectionDict, collection_name: str) -> None:
    locations = collection_dict[collection_name][COLLECTION_VALUE_LOCATIONS]
    storage_devices = ibds_utils.locations_to_storage_devices(locations)

    common_data: list[tuple[str, str]] = []
    table = collection_tablegen.multi(data_dir, collection_name, storage_devices)
    table_items: list[tuple[str, list[Optional[file_tree_snapshot.FileInfo]]]] = ibds_utils.key_sorted_dict_items(table)

    for path, data in table_items:
        for hash_ in sorted(list(set(ibds_tablegen.get_data_hashes(data)))):
            common_data.append((path, hash_))

    save_common_data(common_data, path_generator.gen_common_file_path(collection_name, data_dir))

    hashset = { hash_ for _, hash_ in common_data }
    save_hashset_data(hashset, path_generator.gen_hashset_file_path(collection_name, data_dir))

    hash_table: list[set[str]] = []

    for _ in range(len(storage_devices)):
        hash_table.append(set())

    for path, data in table_items:
        hashes = ibds_tablegen.get_data_hashes_with_none(data)
        for hashes_index in range(len(hashes)):
            hash_ = hashes[hashes_index]
            if hash_ is not None:
                hash_table[hashes_index].add(hash_)

    for hash_table_index in range(len(hash_table)):
        hash_table_item = hash_table[hash_table_index]
        storage_device_ = storage_devices[hash_table_index]
        save_hashset_data(hash_table_item, path_generator.gen_hashset_file_path(collection_name, data_dir, storage_device_))


def generate_collections_definition(data_dir: str, collection_dict: CollectionDict) -> None:
    for collection_name in sorted(collection_dict.keys()):
        _generate_collection_definition(data_dir, collection_dict, collection_name)
