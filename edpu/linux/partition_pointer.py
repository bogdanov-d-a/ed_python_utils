from __future__ import annotations
from .device_pointer import DevicePointer


class PartitionPointer:
    def __init__(self: PartitionPointer, dev: DevicePointer, index: str) -> None:
        self.dev = dev
        self.index = index


    def get_name(self: PartitionPointer, add_dev: bool) -> str:
        return self.dev.get_name(self.index, add_dev)
