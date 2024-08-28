from ..collection import CollectionList
from ..device import Device


def ibds2(file_path: str, devices: list[Device], collections: CollectionList, bundles_path: str) -> None:
    with open(file_path, 'w') as file:
        def head() -> None:
            file.write('''if __name__ == '__main__':
    from edpu import host_alias, storage_finder
    from edpu.ibds2.main import run
    from edpu.ibds2.utils import user_data as UD
    from os.path import abspath, dirname, join

    host_alias_ = host_alias.get()
    storage = storage_finder.find_all_storage().keys()

    storage_devices = {
''')

        head()

        def devices_() -> None:
            for device in devices:
                if not device.use_in_2:
                    continue

                is_scan_available = f'host_alias_ == \'{device.name}\'' if not device.is_removable else f'\'{device.name}\' in storage'
                file.write(f'        \'{device.name}\': {{ UD.IS_REMOVABLE: {str(device.is_removable)}, UD.IS_SCAN_AVAILABLE: {is_scan_available} }},\n')

        devices_()

        def mid() -> None:
            file.write('''    }

    collection_dict = {
''')

        mid()

        def collections_() -> None:
            from ..string_utils import tab_string_list

            def lines() -> list[str]:
                result = []

                for collection_name, collection_data in collections:
                    if collection_data.cd2 is None:
                        continue

                    from ..string_utils import tab_string

                    result += [
                        f'\'{collection_name}\': {{',
                        tab_string('UD.STORAGE_DEVICES: {', 1),
                    ] + list(map(
                            lambda location: tab_string(f'\'{location.storage_device}\': r\'{location.path}\',', 2),
                            collection_data.locations
                    )) + [
                        tab_string('},', 1),
                        tab_string('UD.BUNDLE_SLICES: {', 1),
                    ] + list(map(
                            lambda bundle_slice: tab_string(f'\'{bundle_slice[0]}\': r\'{bundle_slice[1]}\',', 2),
                            collection_data.cd2.bundle_slices
                    )) + [
                        tab_string('},', 1),
                        tab_string('UD.BUNDLE_ALIASES: {', 1),
                    ] + list(map(
                            lambda bundle_alias: tab_string(f'\'{bundle_alias[0]}\': {bundle_alias[1]},', 2),
                            collection_data.cd2.bundle_aliases
                    )) + [
                        tab_string('},', 1),
                        '},',
                    ]

                return result

            file.write('\n'.join(tab_string_list(lines(), 2)))

        collections_()

        def tail() -> None:
            file.write(fr'''
    }}

    apply_bundles = [
    ]

    def diff_tool_handler(a: str, b: str) -> None:
        from subprocess import call
        call([r'C:\Program Files\WinMerge\WinMergeU.exe', '/r', a, b])

    run({{
        UD.STORAGE_DEVICES: storage_devices,
        UD.COLLECTION_DICT: collection_dict,
        UD.DATA_PATH: join(dirname(abspath(__file__)), 'data'),
        UD.BUNDLES_PATH: r'{bundles_path}',
        UD.BUNDLE_SNAPS_PATH: join(dirname(abspath(__file__)), 'bundle_snaps'),
        UD.APPLY_BUNDLES: apply_bundles,
        UD.DIFF_TOOL_HANDLER: diff_tool_handler,
        UD.COLLECTION_PROCESSING_WORKERS: 24,
        UD.SKIP_MTIME: False,
        UD.DEBUG: False,
    }})
''')

        tail()
