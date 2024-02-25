from .user_data import CollectionDict, StorageDevices
from .utils import get_storage_device_list
from edpu import user_interaction


def pick_storage_device(storage_devices: StorageDevices) -> str:
    storage_device_list = get_storage_device_list(storage_devices)
    storage_device_list_cmds = user_interaction.generate_cmds(storage_device_list)
    storage_device_list_cmds_dict = user_interaction.list_to_dict(storage_device_list_cmds)

    str_options = user_interaction.pick_str_option_multi('Choose storage device', storage_device_list_cmds, lambda set_: 'only one device allowed' if len(set_) != 1 else None)
    return storage_device_list_cmds_dict[str_options[0]]


def pick_storage_device_multi(storage_devices: StorageDevices) -> list[str]:
    storage_device_list = get_storage_device_list(storage_devices)
    storage_device_list_cmds = user_interaction.generate_cmds(storage_device_list)
    storage_device_list_cmds_dict = user_interaction.list_to_dict(storage_device_list_cmds)

    result: list[str] = []

    for picked_cmd in user_interaction.pick_str_option_multi('Choose storage devices', storage_device_list_cmds):
        result.append(storage_device_list_cmds_dict[picked_cmd])

    return result


def pick_bundle_alias(bundle_aliases: list[str]) -> str:
    return bundle_aliases[user_interaction.pick_option('Choose bundle alias', bundle_aliases)]


def pick_bundle_slice_alias(bundle_slices: dict[str, str]) -> str:
    bundle_slices_list = list(sorted(bundle_slices.keys()))
    return bundle_slices_list[user_interaction.pick_option('Choose bundle slice alias', bundle_slices_list)]


def pick_collection_alias(collection_dict: CollectionDict) -> str:
    collection_aliases = list(sorted(collection_dict.keys()))
    return collection_aliases[user_interaction.pick_option('Choose collection alias', collection_aliases)]
