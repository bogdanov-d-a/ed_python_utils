if __name__ == '__main__':
    from edpu import host_alias, storage_finder
    from edpu.ibds2.main import run
    from edpu.ibds2.utils import user_data as UD
    from os.path import abspath, dirname, join

    host_alias_ = host_alias.get()
    storage = storage_finder.find_all_storage().keys()

    storage_devices = {
        'PC': { UD.IS_REMOVABLE: False, UD.IS_SCAN_AVAILABLE: host_alias_ == 'PC' },
        'Laptop': { UD.IS_REMOVABLE: False, UD.IS_SCAN_AVAILABLE: host_alias_ == 'Laptop' },
        'USBFlash': { UD.IS_REMOVABLE: True, UD.IS_SCAN_AVAILABLE: 'USBFlash' in storage },
    }

    collection_dict = {
        'Music': {
            UD.STORAGE_DEVICES: {
                'PC': 'C:\\Users\\Username\\Music',
                'Laptop': 'C:\\Users\\Username\\Music',
                'USBFlash': 'Music',
            },
            UD.BUNDLE_SLICES: {
                'Cloud': r'^Cloud\\.*$',
            },
            UD.BUNDLE_ALIASES: {
                'USBFlashSlow': ['Cloud'],
            },
        },
        'Pictures': {
            UD.STORAGE_DEVICES: {
                'PC': 'C:\\Users\\Username\\Pictures',
                'Laptop': 'C:\\Users\\Username\\Pictures',
                'USBFlash': 'Pictures',
            },
            UD.BUNDLE_SLICES: {
                'All': r'.*',
            },
            UD.BUNDLE_ALIASES: {
                'USBFlashSlow': ['All'],
            },
        },
    }

    apply_bundles = [
    ]

    def diff_tool_handler(a: str, b: str) -> None:
        from subprocess import call
        call([r'C:\Program Files\WinMerge\WinMergeU.exe', '/r', a, b])

    run({
        UD.STORAGE_DEVICES: storage_devices,
        UD.COLLECTION_DICT: collection_dict,
        UD.DATA_PATH: join(dirname(abspath(__file__)), 'data'),
        UD.BUNDLES_PATH: r'C:\Users\Username\Downloads\IBDS2Bundles',
        UD.BUNDLE_SNAPS_PATH: join(dirname(abspath(__file__)), 'bundle_snaps'),
        UD.APPLY_BUNDLES: apply_bundles,
        UD.DIFF_TOOL_HANDLER: diff_tool_handler,
        UD.COLLECTION_PROCESSING_WORKERS: 24,
        UD.SKIP_MTIME: False,
        UD.DEBUG: False,
    })
