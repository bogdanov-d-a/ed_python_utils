from ...utils.user_data import CollectionDict


def _generate_collection_definition(data_dir: str, collection_dict: CollectionDict, collection_name: str) -> None:
    from ...impl.definition import save_common_data, save_hashset_data
    from ...impl.file_tree_snapshot import FileInfo
    from ...impl.tablegen import get_data_hashes, get_data_hashes_with_none
    from ...utils.path_generator import gen_common_file_path, gen_hashset_file_path
    from ...utils.user_data import COLLECTION_VALUE_LOCATIONS
    from ...utils.utils import locations_to_storage_devices, key_sorted_dict_items
    from ..tablegen import tablegen
    from typing import Optional

    locations = collection_dict[collection_name][COLLECTION_VALUE_LOCATIONS]
    storage_devices = locations_to_storage_devices(locations)

    common_data: list[tuple[str, str]] = []
    table = tablegen(data_dir, collection_name, storage_devices)
    table_items: list[tuple[str, list[Optional[FileInfo]]]] = key_sorted_dict_items(table)

    for path, data in table_items:
        for hash_ in sorted(list(set(get_data_hashes(data)))):
            common_data.append((path, hash_))

    save_common_data(common_data, gen_common_file_path(collection_name, data_dir))
    save_hashset_data({ hash_ for _, hash_ in common_data }, gen_hashset_file_path(collection_name, data_dir))

    hash_table: list[set[str]] = []

    for _ in range(len(storage_devices)):
        hash_table.append(set())

    for path, data in table_items:
        hashes = get_data_hashes_with_none(data)

        for hashes_index in range(len(hashes)):
            hash_ = hashes[hashes_index]

            if hash_ is not None:
                hash_table[hashes_index].add(hash_)

    for hash_table_index in range(len(hash_table)):
        hash_table_item = hash_table[hash_table_index]
        storage_device_ = storage_devices[hash_table_index]
        save_hashset_data(hash_table_item, gen_hashset_file_path(collection_name, data_dir, storage_device_))


def generate_collections_definition(data_dir: str, collection_dict: CollectionDict) -> None:
    for collection_name in sorted(collection_dict.keys()):
        _generate_collection_definition(data_dir, collection_dict, collection_name)
