from __future__ import annotations
from .user_data import UserData
from typing import Optional


RECYCLE_SUFFIX = 'Recycle'


def path_to_root(path: list[str], root: str) -> str:
    from os import sep
    from os.path import join

    return join(root, sep.join(path))


def get_bundle_file_name(bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    return bundle_alias + '-' + collection_alias + '-' + bundle_slice_alias


def get_bundle_file_path(user_data: UserData, bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    from os.path import join
    return join(user_data.bundles_path, get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias))


def get_bundle_snap_path(user_data: UserData, bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    from os.path import join
    return join(user_data.bundle_snaps_path, get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias) + '.txt')


def get_storage_path(storage_device_name: str, storage_path_cache: dict[str, str]) -> str:
    from ...storage_finder import keep_getting_storage_path

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
    from os.path import join

    if find_data_path:
        abs_data_path = user_data.collection_dict[collection_alias].storage_devices[storage_device_name]
        if user_data.storage_devices[storage_device_name].is_removable:
            abs_data_path = get_storage_path(storage_device_name, storage_path_cache) + abs_data_path
    else:
        abs_data_path = None

    abs_def_path = join(user_data.data_path, collection_alias, storage_device_name)

    return GetCollectionPathsResult(abs_def_path, abs_data_path)
