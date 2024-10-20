from ...utils.storage_device import StorageDevice
from ...utils.user_data import CollectionDict


def _collection_common(data_dir: str, collection_name: str, collection_path: str, skip_paths: list[str]) -> None:
    from ...impl.definition import load_common_data
    from ...utils.path_generator import gen_common_file_path
    from ...utils.utils import key_sorted_dict_items

    data = load_common_data(gen_common_file_path(collection_name, data_dir))
    table: dict[str, list[str]] = {}

    for path, hash_ in data:
        from ...impl.file_tree_snapshot import INDEX_PATH_SEPARATOR
        from ...utils.utils import path_needs_skip

        if path_needs_skip(path.split(INDEX_PATH_SEPARATOR), skip_paths, False):
            continue

        if hash_ not in table:
            table[hash_] = []

        table[hash_].append(path)

    table_items: list[tuple[str, list[str]]] = key_sorted_dict_items(table)

    for hash_, paths in table_items:
        if (len(paths) > 1):
            print(f'REM {hash_}')

            for path in paths:
                from ....string_utils import merge_with_space, quotation_mark_wrap
                from os.path import join

                print(merge_with_space([
                    'REM',
                    'del',
                    '/f',
                    '/q',
                    quotation_mark_wrap(join(collection_path, path)),
                ]))

            print()


def collections_common(data_dir: str, storage_device_: StorageDevice, collection_dict: CollectionDict) -> None:
    from ....storage_finder import keep_getting_storage_path
    from ...utils.user_data import CollectionList
    from ...utils.utils import key_sorted_dict_items

    path_prefix = keep_getting_storage_path(storage_device_.getName()) if storage_device_.isRemovable() else ''
    collection_dict_items: CollectionList = key_sorted_dict_items(collection_dict)

    for collection_name, data in collection_dict_items:
        from ...utils.user_data import COLLECTION_VALUE_LOCATIONS

        for location in data[COLLECTION_VALUE_LOCATIONS]:
            if location.getStorageDevice().getName() == storage_device_.getName():
                from ...utils.user_data import COLLECTION_VALUE_DUPLICATE_SKIP_PATHS
                _collection_common(data_dir, collection_name, path_prefix + location.getPath(), data[COLLECTION_VALUE_DUPLICATE_SKIP_PATHS])
