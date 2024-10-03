from .user_data import CollectionDict, CollectionList, COLLECTION_VALUE_LOCATIONS, COLLECTION_VALUE_SCAN_SKIP_PATHS
from .. import storage_finder
from ..db_lock import DbLock
from . import path_generator
from . import ibds_utils
from . import file_tree_snapshot
from . import storage_device


def _scan_collection_storage_device(data_dir: str, collection_name: str, storage_device_: storage_device.StorageDevice, data_path: str, skip_paths: list[str], skip_mtime: bool) -> None:
    file_tree_snapshot.update_index_file(data_path, path_generator.gen_index_file_path(collection_name, storage_device_, data_dir), skip_paths, skip_mtime)


def scan_storage_device(data_dir: str, collection_dict: CollectionDict, storage_device_: storage_device.StorageDevice, skip_mtime: bool) -> None:
    path_prefix = storage_finder.keep_getting_storage_path(storage_device_.getName()) if storage_device_.isRemovable() else ''

    with DbLock(f'ibds_scan_storage_device_{storage_device_.getLockName()}', 24*60*60):
        collection_dict_items: CollectionList = ibds_utils.key_sorted_dict_items(collection_dict)
        for collection_name, data in collection_dict_items:
            for location in data[COLLECTION_VALUE_LOCATIONS]:
                if location.getStorageDevice().getName() == storage_device_.getName():
                    _scan_collection_storage_device(data_dir, collection_name, storage_device_, path_prefix + location.getPath(), data[COLLECTION_VALUE_SCAN_SKIP_PATHS], skip_mtime)
