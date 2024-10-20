from ..collection import CollectionList
from ..device import Device


def ibds(file_path: str, devices: list[Device], collections: CollectionList) -> None:
    with open(file_path, 'w') as file:
        def head() -> None:
            file.write('''if __name__ == '__main__':
    from edpu import host_alias
    from edpu.ibds.main import run
    from edpu.ibds.utils.location import Location
    from edpu.ibds.utils.storage_device import StorageDevice
    from edpu.ibds.utils.user_data import UserData, CollectionDict
    from edpu.storage_finder import find_all_storage
    from os.path import join, dirname, abspath


''')

        head()

        def devices_() -> None:
            from ..utils import map_device_names, filter_removable_devices

            file.write('    _DEVICES = set([\n')

            for device_name in map_device_names(devices):
                file.write(f'        \'{device_name}\',\n')

            file.write('    ])\n\n')

            file.write('    _DEVICES_REMOVABLE = set([\n')

            for device_name in map_device_names(filter_removable_devices(devices)):
                file.write(f'        \'{device_name}\',\n')

            file.write('    ])\n\n')

            file.write('    _DEVICE_TO_LOCK_NAME = {\n')

            for device in devices:
                file.write(f'        \'{device.name}\': \'{device.lock_name}\',\n')

            file.write('    }\n')

        devices_()

        def mid() -> None:
            file.write('''

    host_alias_ = host_alias.get()
    all_storage = find_all_storage()

    def create_device(name: str) -> StorageDevice:
        if name not in _DEVICES:
            raise Exception('Bad device name')

        return StorageDevice(
            name,
            name in _DEVICES_REMOVABLE,
            (name in _DEVICES_REMOVABLE and name in all_storage) or name == host_alias_,
            _DEVICE_TO_LOCK_NAME[name]
        )

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
                        [str(collection_data.use_descript_ion)],
                    ]

                    result += [f'    \'{collection_name}\': (',] + tab_string_list(aggregate_string_list_list(append_comma_at_last_except_last(nested)), 2) + ['    ),',]

                return result

            file.write('\n'.join(tab_string_list(lines(), 1)))

        collections_()

        def tail() -> None:
            file.write('''
    }


    run(UserData(
        collection_dict,
        devices,
        join(dirname(abspath(__file__)), 'data'),
        False,
        True
    ))
''')

        tail()
