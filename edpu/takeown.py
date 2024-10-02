def takeown_recursive(filename: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    return merge_with_space([
        'takeown',
        '/f',
        quotation_mark_wrap(filename),
        '/r',
        '/d',
        'Y',
    ])
