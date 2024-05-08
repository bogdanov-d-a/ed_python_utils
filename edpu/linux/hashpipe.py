def hashpipe_cmd() -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap
    from .python import python, python_lib

    return merge_with_space([
        python(),
        apostrophe_wrap(python_lib() + '/edpu/runnable/hashpipe.py'),
    ])
