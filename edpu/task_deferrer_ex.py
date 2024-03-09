def get_data(item_keys_all, item_data):
    from . import task_deferrer

    item_data_keys = set()
    for key, _, _ in item_data:
        item_data_keys.add(key)

    item_data_for_td = []
    for key, desc, date in item_data:
        item_data_for_td.append((desc + ' (' + key + ')', date))

    unregistered = item_keys_all - item_data_keys

    return 'Registered:\n' + \
        task_deferrer.get_info(item_data_for_td, show_future=True) + '\n' + \
        'Unregistered:\n' + \
        '\n'.join(sorted(unregistered))
