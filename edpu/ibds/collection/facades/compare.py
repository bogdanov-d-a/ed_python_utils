from ...utils.storage_device import StorageDevice
from ...utils.user_data import CollectionDict


def _storage_devices_to_paths(data_dir: str, collection_name: str, storage_devices: list[StorageDevice]) -> list[str]:
    from ...utils.path_generator import gen_index_file_path

    return list(map(
        lambda storage_device_: gen_index_file_path(collection_name, storage_device_, data_dir),
        storage_devices
    ))


def _multi_storage_devices_of_collection(data_dir: str, collection_name: str, storage_devices: list[StorageDevice], complete_storage_device_indices: set[int]) -> None:
    from ...impl.compare import multi_index_files
    
    multi_index_files(
        _storage_devices_to_paths(data_dir, collection_name, storage_devices),
        complete_storage_device_indices,
        collection_name
    )


def _multi_storage_devices_of_collection_by_hash(data_dir: str, collection_name: str, storage_devices: list[StorageDevice]) -> None:
    from ...impl.compare import multi_index_by_hash_files

    multi_index_by_hash_files(
        _storage_devices_to_paths(data_dir, collection_name, storage_devices),
        collection_name
    )


def _collection(data_dir: str, collection_dict: CollectionDict, collection_name: str, only_available: bool) -> None:
    from ...utils.user_data import COLLECTION_VALUE_LOCATIONS
    from ...utils.utils import locations_to_storage_devices

    locations = collection_dict[collection_name][COLLECTION_VALUE_LOCATIONS]

    _multi_storage_devices_of_collection(
        data_dir,
        collection_name,
        locations_to_storage_devices(locations),
        {
            index
            for _, index
            in filter(
                lambda elem: elem[0].isComplete() and (not only_available or elem[0].getStorageDevice().isScanAvailable()),
                zip(locations, range(len(locations)))
            )
        }
    )


def _collection_by_hash(data_dir: str, collection_dict: CollectionDict, collection_name: str) -> None:
    from ...utils.user_data import COLLECTION_VALUE_LOCATIONS
    from ...utils.utils import locations_to_storage_devices

    _multi_storage_devices_of_collection_by_hash(
        data_dir,
        collection_name,
        locations_to_storage_devices(collection_dict[collection_name][COLLECTION_VALUE_LOCATIONS])
    )


def collections(data_dir: str, collection_dict: CollectionDict, only_available: bool) -> None:
    for collection_name in sorted(collection_dict.keys()):
        _collection(data_dir, collection_dict, collection_name, only_available)


def collections_by_hash(data_dir: str, collection_dict: CollectionDict) -> None:
    for collection_name in sorted(collection_dict.keys()):
        _collection_by_hash(data_dir, collection_dict, collection_name)
