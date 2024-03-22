def del_f_q(path: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    return merge_with_space([
        'del',
        '/f',
        '/q',
        quotation_mark_wrap(path),
    ])
