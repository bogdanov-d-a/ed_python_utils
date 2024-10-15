from ...utils.storage_device import StorageDevice
from ...utils.user_data import CollectionDict


def _scan_collection_storage_device(data_dir: str, collection_name: str, storage_device_: StorageDevice, data_path: str, skip_paths: list[str], skip_mtime: bool) -> None:
    from ...impl.file_tree_snapshot import update_index_file
    from ...utils.path_generator import gen_index_file_path

    update_index_file(
        data_path,
        gen_index_file_path(collection_name, storage_device_, data_dir),
        skip_paths,
        skip_mtime
    )


def scan_storage_device(data_dir: str, collection_dict: CollectionDict, storage_device_: StorageDevice, skip_mtime: bool) -> None:
    from ....db_lock import DbLock
    from ....storage_finder import keep_getting_storage_path

    path_prefix = keep_getting_storage_path(storage_device_.getName()) if storage_device_.isRemovable() else ''

    with DbLock(f'ibds_scan_storage_device_{storage_device_.getLockName()}', 24*60*60):
        from ...utils.user_data import CollectionList
        from ...utils.utils import key_sorted_dict_items

        collection_dict_items: CollectionList = key_sorted_dict_items(collection_dict)

        for collection_name, data in collection_dict_items:
            from ...utils.user_data import COLLECTION_VALUE_LOCATIONS

            for location in data[COLLECTION_VALUE_LOCATIONS]:
                if location.getStorageDevice().getName() == storage_device_.getName():
                    from ...utils.user_data import COLLECTION_VALUE_SCAN_SKIP_PATHS
                    _scan_collection_storage_device(data_dir, collection_name, storage_device_, path_prefix + location.getPath(), data[COLLECTION_VALUE_SCAN_SKIP_PATHS], skip_mtime)
