import re
from typing import Any, Optional
from edpu import user_interaction
from . import location
from . import storage_device


SKIP_PATHS_SEPARATOR = '/'


def key_sorted_dict_items(dict_: dict) -> list[tuple[Any, Any]]:
    return sorted(dict_.items(), key=lambda t: t[0])


def print_lists(lists: list[tuple[str, list[str]]], name: Optional[str]=None) -> None:
    if sum(len(list_[1]) for list_ in lists) == 0:
        return

    if name is not None:
        print(name)

    for list_ in lists:
        if len(list_[1]) == 0:
            continue

        print(list_[0])
        for line in list_[1]:
            print(line)
        print()

    print()


def is_same_list(list_: list[str]) -> bool:
    if len(list_) == 0:
        raise Exception('empty list is not allowed')

    for i in range(len(list_) - 1):
        if (list_[i] != list_[i + 1]):
            return False

    return True


def path_needs_skip(path: list[str], skip_paths: list[str]) -> bool:
    for skip_path in skip_paths:
        if re.match(skip_path, SKIP_PATHS_SEPARATOR.join(path)) is not None:
            return True

    return False


def locations_to_storage_devices(locations: list[location.Location]) -> list[storage_device.StorageDevice]:
    return list(map(lambda location: location.getStorageDevice(), locations))


def pick_storage_device(device_list: list[storage_device.StorageDevice]) -> storage_device.StorageDevice:
    scan_devices = list(filter(lambda device: device.isScanAvailable(), device_list))
    list_ = list(sorted(map(lambda device: device.getName(), scan_devices)))
    dict_ = { device.getName(): device for device in scan_devices }

    return dict_[list_[user_interaction.pick_option('Choose storage device', list_)]]
