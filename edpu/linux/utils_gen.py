def cd(path: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap

    return merge_with_space([
        'cd',
        apostrophe_wrap(path)
    ])


def mkdir(path: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap

    return merge_with_space([
        'mkdir',
        apostrophe_wrap(path)
    ])
