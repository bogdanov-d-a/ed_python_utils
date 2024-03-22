def reg_delete_gen(key: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    return merge_with_space([
        'reg',
        'delete',
        quotation_mark_wrap(key),
        '/f',
    ])


def reg_delete(key: str) -> None:
    from os import system
    system(reg_delete_gen(key))
