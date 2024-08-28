from .path import GetCollectionPathsResult
from .user_data import UserData, StorageDevices
from enum import Enum
from typing import Iterator


class IntersectionType(Enum):
    MATCHING = 0
    DIFFERENT = 1


def intersection(main_list: set[str], aux_list: set[str], type: IntersectionType) -> Iterator[list[str]]:
    from .mappers.path_key import key_to_path

    for main_content in main_list:
        if (main_content in aux_list) == (type == IntersectionType.MATCHING):
            yield key_to_path(main_content)


def get_storage_device_list(storage_devices: StorageDevices, all: bool=False) -> list[str]:
    storage_device_list: list[str] = []

    for device_name, device_data in storage_devices.items():
        if all or device_data.is_scan_available:
            storage_device_list.append(device_name)

    return storage_device_list


def get_bundle_aliases(user_data: UserData) -> list[str]:
    set_: set[str] = set()

    for collection_data in user_data.collection_dict.values():
        set_ |= set(collection_data.bundle_aliases.keys())

    return sorted(set_)


def get_all_aliases_for_storage_device(user_data: UserData, storage_device_name: str, find_data_path: bool=True) -> Iterator[tuple[str, GetCollectionPathsResult]]:
    from .path import get_collection_paths

    storage_path_cache: dict[str, str] = {}

    for collection_alias, collection_data in user_data.collection_dict.items():
        if storage_device_name in collection_data.storage_devices:
            collection_paths = get_collection_paths(user_data, collection_alias, storage_device_name, storage_path_cache, find_data_path)
            yield (collection_alias, collection_paths)
