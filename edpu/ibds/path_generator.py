from __future__ import annotations
from typing import Optional
from . import storage_device
import os


def _gen_impl(data_dir: Optional[str], infixes: list[str]) -> str:
    prefix = data_dir + os.path.sep if data_dir is not None else ''
    return prefix + '-'.join(infixes) + '.txt'


def gen_index_file_path(collection: str, storage_device_: storage_device.StorageDevice, data_dir: Optional[str]) -> str:
    return _gen_impl(data_dir, [collection, storage_device_.getName()])


def gen_common_file_path(collection: str, data_dir: Optional[str]) -> str:
    return _gen_impl(data_dir, [collection, 'Common'])


def gen_hashset_file_path(collection: str, data_dir: Optional[str], storage_device_: Optional[storage_device.StorageDevice]=None) -> str:
    def_ = [collection, 'Hashset']

    if storage_device_ is not None:
        def_.append(storage_device_.getName())

    return _gen_impl(data_dir, def_)
