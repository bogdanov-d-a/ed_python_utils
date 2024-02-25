from __future__ import annotations
import os
import shutil
from typing import Callable, Iterator, Optional
from .mappers.type_prefix import type_to_prefix, prefix_to_type
from .mappers.path_key import key_to_path
from ..user_data import UserData, StorageDevices, CollectionDict
from edpu import file_hashing
from edpu import user_interaction
from edpu import storage_finder


def def_path_to_data_path(def_path: list[str]) -> tuple[str, list[str]]:
    type_ = prefix_to_type(def_path[-1][0])
    data_path = list(map(lambda a: a[1:], def_path[:-1])) + [def_path[-1][1:]]
    return type_, data_path


def data_path_to_def_path(path_: list[str], type_: str) -> list[str]:
    return list(map(lambda a: '_' + a, path_[:-1])) + [type_to_prefix(type_) + path_[-1]]


def hash_file(path: str) -> str:
    print('Calculating hash for ' + path)
    return file_hashing.sha512_file(path)


def getmtime(path: str, progress_fn: Callable[[], None]) -> float:
    progress_fn()
    return os.path.getmtime(path)


def make_getmtime_progress_printer(path_: str) -> Callable[[], None]:
    return make_count_printer('getmtime', path_)


def setmtime(path: str, time: float, progress_fn: Callable[[], None]) -> None:
    progress_fn()
    os.utime(path, (time, time))


def make_setmtime_progress_printer(path_: str) -> Callable[[], None]:
    return make_count_printer('setmtime', path_)


def make_count_printer(annotation: str, path_: str) -> Callable[[], None]:
    from edpu.throttling import TimeBasedAggregator
    return TimeBasedAggregator.make_count_printer(0.5, f'{annotation} {path_}')


def path_to_root(path: list[str], root: str) -> str:
    return os.path.join(root, os.sep.join(path))


def makedirs_helper(path: list[str], root: str, is_file: bool) -> None:
    if is_file:
        if len(path) <= 1:
            return
        path = path[:-1]

    os.makedirs(path_to_root(path, root), exist_ok=True)


def intersection_handler(main_list: set[str], aux_list: set[str], use_intersection: bool, action: Callable[[list[str]], None]) -> None:
    for main_content in main_list:
        if (main_content in aux_list) == use_intersection:
            action(key_to_path(main_content))


def get_storage_device_list(storage_devices: StorageDevices) -> list[str]:
    storage_device_list: list[str] = []

    for device_name, device_data in storage_devices.items():
        if device_data.is_scan_available:
            storage_device_list.append(device_name)

    return storage_device_list


def pick_storage_device(storage_devices: StorageDevices) -> str:
    storage_device_list = get_storage_device_list(storage_devices)
    storage_device_list_cmds: list[tuple[str, str]] = user_interaction.generate_cmds(storage_device_list)
    storage_device_list_cmds_dict: dict[str, str] = user_interaction.list_to_dict(storage_device_list_cmds)

    str_options = user_interaction.pick_str_option_multi('Choose storage device', storage_device_list_cmds, lambda set_: 'only one device allowed' if len(set_) != 1 else None)
    return storage_device_list_cmds_dict[str_options[0]]


def pick_storage_device_multi(storage_devices: StorageDevices) -> list[str]:
    storage_device_list = get_storage_device_list(storage_devices)
    storage_device_list_cmds: list[tuple[str, str]] = user_interaction.generate_cmds(storage_device_list)
    storage_device_list_cmds_dict: dict[str, str] = user_interaction.list_to_dict(storage_device_list_cmds)

    result: list[str] = []

    for picked_cmd in user_interaction.pick_str_option_multi('Choose storage devices', storage_device_list_cmds):
        result.append(storage_device_list_cmds_dict[picked_cmd])

    return result


def get_bundle_aliases(user_data: UserData) -> list[str]:
    set_: set[str] = set()

    for collection_data in user_data.collection_dict.values():
        set_ |= set(collection_data.bundle_aliases.keys())

    return sorted(set_)


def pick_bundle_alias(bundle_aliases: list[str]) -> str:
    return bundle_aliases[user_interaction.pick_option('Choose bundle alias', bundle_aliases)]


def pick_bundle_slice_alias(bundle_slices: dict[str, str]) -> str:
    bundle_slices_list = list(sorted(bundle_slices.keys()))
    return bundle_slices_list[user_interaction.pick_option('Choose bundle slice alias', bundle_slices_list)]


def pick_collection_alias(collection_dict: CollectionDict) -> str:
    collection_aliases = list(sorted(collection_dict.keys()))
    return collection_aliases[user_interaction.pick_option('Choose collection alias', collection_aliases)]


def get_storage_path(storage_device_name: str, storage_path_cache: dict[str, str]) -> str:
    storage_path = storage_path_cache.get(storage_device_name)

    if storage_path is not None:
        return storage_path

    storage_path = storage_finder.keep_getting_storage_path(storage_device_name)
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
    if os.path.exists(dst):
        raise Exception('copy_no_overwrite')

    shutil.copy(src, dst)
