from __future__ import annotations
from . import storage_device


class Location:
    def __init__(self: Location, storage_device_: storage_device.StorageDevice, path: str, is_complete: bool) -> None:
        self._storage_device = storage_device_
        self._path = path
        self._is_complete = is_complete

    def getStorageDevice(self: Location) -> storage_device.StorageDevice:
        return self._storage_device

    def getPath(self: Location) -> str:
        return self._path

    def isComplete(self: Location) -> bool:
        return self._is_complete
