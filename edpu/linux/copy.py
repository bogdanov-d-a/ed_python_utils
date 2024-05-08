def copy_recursive(src: str, dst: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap

    return merge_with_space([
        'cp',
        '-r',
        apostrophe_wrap(src),
        apostrophe_wrap(dst),
    ])
