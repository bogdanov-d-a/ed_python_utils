from typing import Optional
from . import file_tree_snapshot
from . import ibds_tablegen
from . import path_generator
from . import storage_device


def multi(data_dir: str, collection_name: str, storage_devices: list[storage_device.StorageDevice]) -> dict[str, list[Optional[file_tree_snapshot.FileInfo]]]:
    paths = list(map(lambda storage_device_: path_generator.gen_index_file_path(collection_name, storage_device_, data_dir), storage_devices))
    return ibds_tablegen.index_files(paths)
