from ...utils.user_data import UserData


def create_bundle(user_data: UserData) -> None:
    from ....guided_directory_use import PathKeeper

    with PathKeeper(user_data.bundles_path):
        from ...utils import user_interaction
        from ...utils.utils import get_bundle_aliases

        storage_device = user_interaction.pick_storage_device(user_data.storage_devices)
        bundle_alias = user_interaction.pick_bundle_alias(get_bundle_aliases(user_data))

        for collection_alias, collection_data in user_data.collection_dict.items():
            if bundle_alias not in collection_data.bundle_aliases:
                continue

            for bundle_slice_alias in collection_data.bundle_aliases[bundle_alias]:
                from ...impl.bundle.create import create_bundle as impl

                impl(user_data, storage_device, bundle_alias, collection_alias, bundle_slice_alias)
                print(collection_alias + ' - ' + bundle_slice_alias)
                input()
