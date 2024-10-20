from ...utils.storage_device import StorageDevice
from ...utils.user_data import CollectionDict


def _descript_ion_collect(data_dir: str, collection_name: str, data_path: str, use_descript_ion: bool) -> None:
    if not use_descript_ion:
        return

    from ...impl.descript_ion_collect import descript_ion_collect as impl
    from ...utils.path_generator import gen_common_file_path, gen_descript_ion_file_path

    impl(
        data_path,
        gen_common_file_path(collection_name, data_dir),
        gen_descript_ion_file_path(collection_name, data_dir)
    )


def descript_ion_collect(data_dir: str, collection_dict: CollectionDict, storage_device_: StorageDevice) -> None:
    from ....storage_finder import keep_getting_storage_path
    from ...utils.user_data import CollectionList
    from ...utils.utils import key_sorted_dict_items

    path_prefix = keep_getting_storage_path(storage_device_.getName()) if storage_device_.isRemovable() else ''

    collection_dict_items: CollectionList = key_sorted_dict_items(collection_dict)

    for collection_name, data in collection_dict_items:
        from ...utils.user_data import COLLECTION_VALUE_LOCATIONS

        for location in data[COLLECTION_VALUE_LOCATIONS]:
            if location.getStorageDevice().getName() == storage_device_.getName():
                from ...utils.user_data import COLLECTION_VALUE_USE_DESCRIPT_ION
                _descript_ion_collect(data_dir, collection_name, path_prefix + location.getPath(), data[COLLECTION_VALUE_USE_DESCRIPT_ION])
