from edpu_user import storage_path_data
from edpu_user import host_path_data
from . import host_alias
from .storage_finder import find_all_storage


def get_storage_data_impl(stor_alias, root_path):
    stor_alias_data = storage_path_data.get().get(stor_alias)
    if stor_alias_data is None:
        return None

    result = {}
    for col_alias, path in stor_alias_data.items():
        result[col_alias] = root_path + path
    return result


def get_storage_data_auto(alias):
    path = find_all_storage().get(alias)
    if path is None:
        return None
    return get_storage_data_impl(alias, path)


def get_host_data():
    return host_path_data.get().get(host_alias.get())
