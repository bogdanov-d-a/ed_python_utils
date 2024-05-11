def f7z_extract(path: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap

    return merge_with_space([
        '7z',
        'x',
        apostrophe_wrap(path),
    ])
