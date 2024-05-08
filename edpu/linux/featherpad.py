def featherpad() -> str:
    return 'featherpad'


def featherpad_open(path: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap

    return merge_with_space([
        featherpad(),
        apostrophe_wrap(path)
    ])
