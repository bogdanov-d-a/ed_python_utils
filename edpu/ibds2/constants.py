from typing import Any
from edpu.file_tree_walker import TYPE_DIR, TYPE_FILE


INDEX_PATH_SEPARATOR = '\\'


debug = False


IS_REMOVABLE_KEY = 'is_removable'
IS_SCAN_AVAILABLE_KEY = 'is_scan_available'
STORAGE_DEVICES_KEY = 'storage_devices'
BUNDLE_ALIASES_KEY = 'bundle_aliases'
BUNDLE_SLICES_KEY = 'bundle_slices'
COLLECTION_DICT_KEY = 'collection_dict'
DATA_PATH_KEY = 'data_path'
BUNDLES_PATH_KEY = 'bundles_path'
BUNDLE_SNAPS_PATH_KEY = 'bundle_snaps_path'
APPLY_BUNDLES_KEY = 'apply_bundles'
DEF_PATH_KEY = 'def_path'
DIFF_TOOL_HANDLER = 'diff_tool_handler'
COLLECTION_PROCESSING_WORKERS = 'collection_processing_workers'
SKIP_MTIME = 'skip_mtime'


UserData = dict[str, Any]
StorageDevices = dict[str, dict[str, Any]]
CollectionDict = dict[str, dict[str, Any]]
CollectionStorageDevices = dict[str, str]
