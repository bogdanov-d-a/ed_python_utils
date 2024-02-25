from ...utils.user_data import UserData


def create_bundle(user_data: UserData) -> None:
    from ...impl.bundle.create import create_bundle as impl
    from ...utils import utils
    from edpu import guided_directory_use

    def bundles_path_callback(_) -> None:
        storage_device = utils.pick_storage_device(user_data.storage_devices)
        bundle_alias = utils.pick_bundle_alias(utils.get_bundle_aliases(user_data))

        for collection_alias, collection_data in user_data.collection_dict.items():
            if bundle_alias not in collection_data.bundle_aliases:
                continue

            for bundle_slice_alias in collection_data.bundle_aliases[bundle_alias]:
                impl(user_data, storage_device, bundle_alias, collection_alias, bundle_slice_alias)
                print(collection_alias + ' - ' + bundle_slice_alias)
                input()

    guided_directory_use.run_with_path(user_data.bundles_path, bundles_path_callback)
