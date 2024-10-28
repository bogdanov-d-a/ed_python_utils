def rm_rf(path: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap

    return merge_with_space([
        'rm',
        '-rf',
        apostrophe_wrap(path),
    ])
