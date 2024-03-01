from .user_data import CollectionDict, COLLECTION_VALUE_LOCATIONS
from . import ibds_compare
from . import ibds_utils
from . import path_generator
from . import storage_device


def _storage_devices_to_paths(data_dir: str, collection_name: str, storage_devices: list[storage_device.StorageDevice]) -> list[str]:
    return list(map(lambda storage_device_: path_generator.gen_index_file_path(collection_name, storage_device_, data_dir), storage_devices))


def _multi_storage_devices_of_collection(data_dir: str, collection_name: str, storage_devices: list[storage_device.StorageDevice], complete_storage_device_indices: set[int]) -> None:
    paths = _storage_devices_to_paths(data_dir, collection_name, storage_devices)
    ibds_compare.multi_index_files(paths, complete_storage_device_indices, collection_name)


def _multi_storage_devices_of_collection_by_hash(data_dir: str, collection_name: str, storage_devices: list[storage_device.StorageDevice]) -> None:
    paths = _storage_devices_to_paths(data_dir, collection_name, storage_devices)
    ibds_compare.multi_index_by_hash_files(paths, collection_name)


def _collection(data_dir: str, collection_dict: CollectionDict, collection_name: str, only_available: bool) -> None:
    locations = collection_dict[collection_name][COLLECTION_VALUE_LOCATIONS]
    complete_location_indices = { index for _, index in filter(lambda elem: elem[0].isComplete() and (not only_available or elem[0].getStorageDevice().isScanAvailable()), zip(locations, range(len(locations)))) }
    _multi_storage_devices_of_collection(data_dir, collection_name, ibds_utils.locations_to_storage_devices(locations), complete_location_indices)


def _collection_by_hash(data_dir: str, collection_dict: CollectionDict, collection_name: str) -> None:
    locations = collection_dict[collection_name][COLLECTION_VALUE_LOCATIONS]
    _multi_storage_devices_of_collection_by_hash(data_dir, collection_name, ibds_utils.locations_to_storage_devices(locations))


def collections(data_dir: str, collection_dict: CollectionDict, only_available: bool) -> None:
    for collection_name in sorted(collection_dict.keys()):
        _collection(data_dir, collection_dict, collection_name, only_available)


def collections_by_hash(data_dir: str, collection_dict: CollectionDict) -> None:
    for collection_name in sorted(collection_dict.keys()):
        _collection_by_hash(data_dir, collection_dict, collection_name)
