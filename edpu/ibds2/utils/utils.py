from __future__ import annotations
from .user_data import UserData, StorageDevices
from typing import Callable, Iterator, Optional
import os


def hash_file(path: str) -> str:
    from edpu.file_hashing import sha512_file

    print('Calculating hash for ' + path)
    return sha512_file(path)


def path_to_root(path: list[str], root: str) -> str:
    return os.path.join(root, os.sep.join(path))


def makedirs_helper(path: list[str], root: str, is_file: bool) -> None:
    if is_file:
        if len(path) <= 1:
            return
        path = path[:-1]

    os.makedirs(path_to_root(path, root), exist_ok=True)


def intersection_handler(main_list: set[str], aux_list: set[str], use_intersection: bool, action: Callable[[list[str]], None]) -> None:
    from .mappers.path_key import key_to_path

    for main_content in main_list:
        if (main_content in aux_list) == use_intersection:
            action(key_to_path(main_content))


def get_storage_device_list(storage_devices: StorageDevices) -> list[str]:
    storage_device_list: list[str] = []

    for device_name, device_data in storage_devices.items():
        if device_data.is_scan_available:
            storage_device_list.append(device_name)

    return storage_device_list


def get_bundle_aliases(user_data: UserData) -> list[str]:
    set_: set[str] = set()

    for collection_data in user_data.collection_dict.values():
        set_ |= set(collection_data.bundle_aliases.keys())

    return sorted(set_)


def get_storage_path(storage_device_name: str, storage_path_cache: dict[str, str]) -> str:
    from edpu.storage_finder import keep_getting_storage_path

    storage_path = storage_path_cache.get(storage_device_name)

    if storage_path is not None:
        return storage_path

    storage_path = keep_getting_storage_path(storage_device_name)
    storage_path_cache[storage_device_name] = storage_path
    return storage_path


class GetCollectionPathsResult:
    def __init__(self: GetCollectionPathsResult, def_: str, data: Optional[str]) -> None:
        self.def_ = def_
        self._data = data

    def get_data(self: GetCollectionPathsResult) -> str:
        if self._data is None:
            raise Exception()
        return self._data


def get_collection_paths(user_data: UserData, collection_alias: str, storage_device_name: str, storage_path_cache: dict[str, str], find_data_path: bool=True) -> GetCollectionPathsResult:
    if find_data_path:
        abs_data_path = user_data.collection_dict[collection_alias].storage_devices[storage_device_name]
        if user_data.storage_devices[storage_device_name].is_removable:
            abs_data_path = get_storage_path(storage_device_name, storage_path_cache) + abs_data_path
    else:
        abs_data_path = None

    abs_def_path = os.path.join(user_data.data_path, collection_alias, storage_device_name)

    return GetCollectionPathsResult(abs_def_path, abs_data_path)


def get_bundle_file_name(bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    return bundle_alias + '-' + collection_alias + '-' + bundle_slice_alias


def get_bundle_file_path(user_data: UserData, bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    return os.path.join(user_data.bundles_path, get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias))


def get_bundle_snap_path(user_data: UserData, bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    return os.path.join(user_data.bundle_snaps_path, get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias) + '.txt')


def get_all_aliases_for_storage_device(user_data: UserData, storage_device_name: str, find_data_path: bool=True) -> Iterator[tuple[str, GetCollectionPathsResult]]:
    storage_path_cache: dict[str, str] = {}

    for collection_alias, collection_data in user_data.collection_dict.items():
        if storage_device_name in collection_data.storage_devices:
            collection_paths = get_collection_paths(user_data, collection_alias, storage_device_name, storage_path_cache, find_data_path)
            yield (collection_alias, collection_paths)


def copy_no_overwrite(src: str, dst: str) -> None:
    from shutil import copy

    if os.path.exists(dst):
        raise Exception('copy_no_overwrite')

    copy(src, dst)
