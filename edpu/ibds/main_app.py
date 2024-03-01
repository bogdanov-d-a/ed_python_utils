from typing import Callable
from edpu import user_interaction
from edpu import pause_at_end
from . import collection_scanner
from . import collection_file_set
from . import collection_compare
from . import collection_definition
from . import duplicate_finder
from . import ibds_utils
from . import user_data


def run(user_data: user_data.UserData) -> None:
    def main() -> None:
        def scan_storage_device() -> None:
            storage_device_ = ibds_utils.pick_storage_device(user_data.getDeviceList())
            collection_scanner.scan_storage_device(user_data.getDataPath(), user_data.getCollectionDict(), storage_device_, user_data.getSkipMtime())

        actions: list[tuple[str, str, Callable[[], None]]] = [
            ('s', 'Scan location', scan_storage_device),
            ('c', 'Compare all data', lambda: collection_compare.collections(user_data.getDataPath(), user_data.getCollectionDict(), user_data.getCompareOnlyAvailable())),
            ('g', 'Generate collection definitions', lambda: collection_definition.generate_collections_definition(user_data.getDataPath(), user_data.getCollectionDict())),
            ('d', 'Find file duplicates', lambda: duplicate_finder.collections_common(user_data.getDataPath(), user_data.getCollectionDict())),
            ('f', 'Check data file set', lambda: collection_file_set.check_data_file_set(user_data.getDataPath(), user_data.getCollectionDict())),
            ('u', 'Find unique data', lambda: collection_compare.collections_by_hash(user_data.getDataPath(), user_data.getCollectionDict())),
        ]

        action: Callable[[], None] = user_interaction.pick_str_option_ex('Choose an action', actions)
        action()

    pause_at_end.run(main, 'Program completed successfully')
