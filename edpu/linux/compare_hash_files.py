def compare_hash_files(a: str, b: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap
    from .python import python, python_lib

    return merge_with_space([
        python(),
        apostrophe_wrap(python_lib() + '/edpu/launchers/compare_hash_files.py'),
        apostrophe_wrap(a),
        apostrophe_wrap(b),
    ])
