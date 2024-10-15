from __future__ import annotations


class StorageDevice:
    def __init__(self: StorageDevice, name: str, is_removable: bool, is_scan_available: bool, lock_name: str) -> None:
        self._name = name
        self._is_removable = is_removable
        self._is_scan_available = is_scan_available
        self._lock_name = lock_name

    def getName(self: StorageDevice) -> str:
        return self._name

    def isRemovable(self: StorageDevice) -> bool:
        return self._is_removable

    def isScanAvailable(self: StorageDevice) -> bool:
        return self._is_scan_available

    def getLockName(self: StorageDevice) -> str:
        return self._lock_name
