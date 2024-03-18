def start_d(cwd: str, cmd: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    return merge_with_space([
        'start',
        '/d',
        quotation_mark_wrap(cwd),
        cmd,
    ])
