from __future__ import annotations
from .location import Location
from .storage_device import StorageDevice


COLLECTION_VALUE_LOCATIONS = 0
COLLECTION_VALUE_SCAN_SKIP_PATHS = 1
COLLECTION_VALUE_DUPLICATE_SKIP_PATHS = 2


CollectionValue = tuple[list[Location], list[str], list[str]]
CollectionDict = dict[str, CollectionValue]
CollectionList = list[tuple[str, CollectionValue]]


class UserData:
    def __init__(
            self: UserData,
            collection_dict: CollectionDict,
            device_list: list[StorageDevice],
            data_path: str,
            skip_mtime: bool,
            compare_only_available: bool
    ) -> None:
        self._collection_dict = collection_dict
        self._device_list = device_list
        self._data_path = data_path
        self._skip_mtime = skip_mtime
        self._compare_only_available = compare_only_available

    def getCollectionDict(self: UserData) -> CollectionDict:
        return self._collection_dict

    def getDeviceList(self: UserData) -> list[StorageDevice]:
        return self._device_list

    def getDataPath(self: UserData) -> str:
        return self._data_path

    def getSkipMtime(self: UserData) -> bool:
        return self._skip_mtime

    def getCompareOnlyAvailable(self: UserData) -> bool:
        return self._compare_only_available
