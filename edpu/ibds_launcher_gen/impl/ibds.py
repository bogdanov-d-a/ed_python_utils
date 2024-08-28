from ..collection import CollectionList
from ..device import Device


def ibds(file_path: str, devices: list[Device], collections: CollectionList) -> None:
    with open(file_path, 'w') as file:
        def head() -> None:
            file.write('''from edpu import host_alias
from edpu import storage_finder
from edpu.ibds.storage_device import StorageDevice
from edpu.ibds.location import Location
from edpu.ibds.user_data import UserData, CollectionDict
from edpu.ibds import main_app
import os


''')

        head()

        def devices_() -> None:
            from ..utils import map_device_names, filter_removable_devices

            file.write(f'_DEVICES = set({map_device_names(devices)})\n')
            file.write(f'_DEVICES_REMOVABLE = set({map_device_names(filter_removable_devices(devices))})\n')

        devices_()

        def mid() -> None:
            file.write('''

host_alias_ = host_alias.get()
all_storage = storage_finder.find_all_storage()

def create_device(name):
    if name not in _DEVICES:
        raise Exception('Bad device name')
    return StorageDevice(name, name in _DEVICES_REMOVABLE, (name in _DEVICES_REMOVABLE and name in all_storage) or name == host_alias_)

devices = []
for name in _DEVICES:
    devices.append(create_device(name))


collection_dict: CollectionDict = {
''')

        mid()

        def collections_() -> None:
            from ..string_utils import tab_string_list

            def lines() -> list[str]:
                result = []

                for collection_name, collection_data in collections:
                    from ..string_utils import get_list_lines, get_list_lines_of_raw_strings, aggregate_string_list_list, append_comma_at_last_except_last

                    nested = [
                        get_list_lines(list(map(
                            lambda location: f'Location(create_device(\'{location.storage_device}\'), r\'{location.path}\', {location.is_complete})',
                            collection_data.locations
                        ))),
                        get_list_lines_of_raw_strings(collection_data.scan_skip_paths),
                        get_list_lines_of_raw_strings(collection_data.duplicate_skip_paths),
                    ]

                    result += [f'\'{collection_name}\': (',] + tab_string_list(aggregate_string_list_list(append_comma_at_last_except_last(nested)), 1) + ['),',]

                return result

            file.write('\n'.join(tab_string_list(lines(), 1)))

        collections_()

        def tail() -> None:
            file.write('''
}


data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
main_app.run(UserData(collection_dict, devices, data_path, False, True))
''')

        tail()
