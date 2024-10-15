from ..impl.file_tree_snapshot import FileInfo
from ..utils.storage_device import StorageDevice
from typing import Optional


def tablegen(data_dir: str, collection_name: str, storage_devices: list[StorageDevice]) -> dict[str, list[Optional[FileInfo]]]:
    from ..impl.tablegen import index_files
    from ..utils.path_generator import gen_index_file_path

    return index_files(list(map(
        lambda storage_device_: gen_index_file_path(collection_name, storage_device_, data_dir),
        storage_devices
    )))
