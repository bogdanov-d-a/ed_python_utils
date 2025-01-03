from ...utils import time
from ...utils.storage_device import StorageDevice
from ...utils.user_data import CollectionDict


def _scan_collection_storage_device(data_dir: str, collection_name: str, storage_device_: StorageDevice, data_path: str, skip_paths: list[str], force_rescan: bool, use_descript_ion: bool, skip_mtime: bool, collector: time.Collector) -> None:
    from ...impl.file_tree_snapshot import update_index_file
    from ...utils.path_generator import gen_index_file_path

    update_index_file(
        data_path,
        gen_index_file_path(collection_name, storage_device_, data_dir),
        skip_paths,
        force_rescan,
        use_descript_ion,
        skip_mtime,
        collector
    )


def scan_storage_device(data_dir: str, collection_dict: CollectionDict, storage_device_: StorageDevice, force_rescan: bool, skip_mtime: bool) -> None:
    from ....db_lock import DbLock
    from ....storage_finder import keep_getting_storage_path

    path_prefix = keep_getting_storage_path(storage_device_.getName()) if storage_device_.isRemovable() else ''

    with time.CollectorPrinter() as collector:
        with time.get_perf_counter_measure(collector, time.Key.MAIN_WITH_LOCK):
            with DbLock(f'ibds_scan_storage_device_{storage_device_.getLockName()}', 24*60*60):
                with time.get_perf_counter_measure(collector, time.Key.MAIN):
                    from ...utils.user_data import CollectionList
                    from ...utils.utils import key_sorted_dict_items

                    collection_dict_items: CollectionList = key_sorted_dict_items(collection_dict)

                    for collection_name, data in collection_dict_items:
                        from ...utils.user_data import COLLECTION_VALUE_LOCATIONS

                        for location in data[COLLECTION_VALUE_LOCATIONS]:
                            if location.getStorageDevice().getName() == storage_device_.getName():
                                from ...utils.user_data import COLLECTION_VALUE_SCAN_SKIP_PATHS, COLLECTION_VALUE_USE_DESCRIPT_ION
                                _scan_collection_storage_device(data_dir, collection_name, storage_device_, path_prefix + location.getPath(), data[COLLECTION_VALUE_SCAN_SKIP_PATHS], force_rescan, data[COLLECTION_VALUE_USE_DESCRIPT_ION], skip_mtime, collector)
