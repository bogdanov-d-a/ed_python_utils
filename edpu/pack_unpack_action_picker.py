def pick_action() -> bool:
    from .user_interaction import pick_str_option, list_to_dict

    pack_char = 'p'

    return pick_str_option(
        'Pick action',
        list_to_dict([
            (pack_char, 'Pack'),
            ('u', 'Unpack'),
        ])
    ) == pack_char
