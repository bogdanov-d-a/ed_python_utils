from __future__ import annotations
from . import device
from typing import Optional


class DevicePointer:
    def __init__(self: DevicePointer, type: device.Type, index: str, nvme_index: Optional[str]) -> None:
        self.type = type
        self.index = index
        self.nvme_index = nvme_index


    def get_name(self: DevicePointer, part_index: Optional[str], add_dev: bool) -> str:
        return device.get(self.type, self.index, self.nvme_index, part_index, add_dev)
