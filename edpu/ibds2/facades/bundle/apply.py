from ...utils.user_data import UserData


def apply_bundle(user_data: UserData) -> None:
    from ...impl.bundle.apply import apply_bundle as impl
    from ...utils import utils

    storage_device = utils.pick_storage_device(user_data.storage_devices)
    collection_alias = utils.pick_collection_alias(user_data.collection_dict)
    bundle_slice_alias = utils.pick_bundle_slice_alias(user_data.collection_dict[collection_alias].bundle_slices)

    impl(user_data, storage_device, collection_alias, bundle_slice_alias, user_data.apply_bundles)
