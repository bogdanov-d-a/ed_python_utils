ICACLS = 'icacls'


def icacls_view(path: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    return merge_with_space([
        ICACLS,
        quotation_mark_wrap(path),
    ])


def icacls_reset(path: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    return merge_with_space([
        ICACLS,
        quotation_mark_wrap(path),
        '/reset',
        '/t',
        '/c',
        '/l',
        '/q',
    ])
