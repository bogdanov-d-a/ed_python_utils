from __future__ import annotations
from typing import Any, Callable


IS_REMOVABLE_KEY = 'is_removable'
IS_SCAN_AVAILABLE_KEY = 'is_scan_available'
STORAGE_DEVICES_KEY = 'storage_devices'
BUNDLE_ALIASES_KEY = 'bundle_aliases'
BUNDLE_SLICES_KEY = 'bundle_slices'
COLLECTION_DICT_KEY = 'collection_dict'
DATA_PATH_KEY = 'data_path'
BUNDLES_PATH_KEY = 'bundles_path'
BUNDLE_SNAPS_PATH_KEY = 'bundle_snaps_path'
APPLY_BUNDLES_KEY = 'apply_bundles'
DIFF_TOOL_HANDLER = 'diff_tool_handler'
COLLECTION_PROCESSING_WORKERS = 'collection_processing_workers'
SKIP_MTIME = 'skip_mtime'
DEBUG = 'debug'


DiffToolHandler = Callable[[str, str], None]


class UserData:
    def __init__(self: UserData, data: dict[str, Any]) -> None:
        self.storage_devices = UserData.get_storage_devices(data[STORAGE_DEVICES_KEY])
        self.collection_dict = UserData.get_collection_dict(data[COLLECTION_DICT_KEY])
        self.data_path: str = data[DATA_PATH_KEY]
        self.bundles_path: str = data[BUNDLES_PATH_KEY]
        self.bundle_snaps_path: str = data[BUNDLE_SNAPS_PATH_KEY]
        self.apply_bundles: list[str] = data[APPLY_BUNDLES_KEY]
        self.diff_tool_handler: DiffToolHandler = data[DIFF_TOOL_HANDLER]
        self.collection_processing_workers: int = data[COLLECTION_PROCESSING_WORKERS]
        self.skip_mtime: bool = data[SKIP_MTIME]
        self.debug: bool = data[DEBUG]

    @staticmethod
    def get_storage_devices(data: dict[str, dict[str, Any]]) -> StorageDevices:
        return {
            name: StorageDevice(data_)
            for name, data_ in data.items()
        }

    @staticmethod
    def get_collection_dict(data: dict[str, dict[str, Any]]) -> CollectionDict:
        return {
            name: Collection(data_)
            for name, data_ in data.items()
        }


class StorageDevice:
    def __init__(self: StorageDevice, data: dict[str, Any]) -> None:
        self.is_removable: bool = data[IS_REMOVABLE_KEY]
        self.is_scan_available: bool = data[IS_SCAN_AVAILABLE_KEY]


StorageDevices = dict[str, StorageDevice]


class Collection:
    def __init__(self: Collection, data: dict[str, Any]) -> None:
        self.storage_devices: dict[str, str] = data[STORAGE_DEVICES_KEY]
        self.bundle_slices: dict[str, str] = data[BUNDLE_SLICES_KEY]
        self.bundle_aliases: dict[str, list[str]] = data[BUNDLE_ALIASES_KEY]


CollectionDict = dict[str, Collection]
