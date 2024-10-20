from .utils.user_data import UserData


def run(user_data: UserData) -> None:
    from .. import pause_at_end

    def main() -> None:
        from ..user_interaction import pick_str_option_ex
        from .collection.facades.check_file_set import check_data_file_set
        from .collection.facades.compare import collections, collections_by_hash
        from .collection.facades.generate_definition import generate_collections_definition
        from .utils.utils import DESCRIPT_ION

        def scan_storage_device() -> None:
            from .collection.facades.scan import scan_storage_device as impl
            from .utils.utils import pick_storage_device

            storage_device_ = pick_storage_device(user_data.getDeviceList())
            impl(user_data.getDataPath(), user_data.getCollectionDict(), storage_device_, user_data.getSkipMtime())

        def find_file_duplicates() -> None:
            from .collection.facades.find_duplicates import collections_common
            from .utils.utils import pick_storage_device

            storage_device_ = pick_storage_device(user_data.getDeviceList())
            collections_common(user_data.getDataPath(), storage_device_, user_data.getCollectionDict())

        def descript_ion_collect() -> None:
            from .collection.facades.descript_ion_collect import descript_ion_collect as impl
            from .utils.utils import pick_storage_device

            storage_device_ = pick_storage_device(user_data.getDeviceList())
            impl(user_data.getDataPath(), user_data.getCollectionDict(), storage_device_)

        def descript_ion_apply() -> None:
            from .collection.facades.descript_ion_apply import descript_ion_apply as impl
            from .utils.utils import pick_storage_device

            storage_device_ = pick_storage_device(user_data.getDeviceList())
            impl(user_data.getDataPath(), user_data.getCollectionDict(), storage_device_)

        pick_str_option_ex('Choose an action', [
            ('s', 'Scan location', scan_storage_device),
            ('c', 'Compare all data', lambda: collections(user_data.getDataPath(), user_data.getCollectionDict(), user_data.getCompareOnlyAvailable())),
            ('g', 'Generate collection definitions', lambda: generate_collections_definition(user_data.getDataPath(), user_data.getCollectionDict())),
            ('d', 'Find file duplicates', find_file_duplicates),
            ('f', 'Check data file set', lambda: check_data_file_set(user_data.getDataPath(), user_data.getCollectionDict())),
            ('u', 'Find unique data', lambda: collections_by_hash(user_data.getDataPath(), user_data.getCollectionDict())),
            ('dc', f'{DESCRIPT_ION} collect', descript_ion_collect),
            ('da', f'{DESCRIPT_ION} apply', descript_ion_apply),
        ])()

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
