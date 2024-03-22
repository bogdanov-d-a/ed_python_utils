def taskkill_f_im_gen(name: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    return merge_with_space([
        'taskkill',
        '/f',
        '/im',
        quotation_mark_wrap(name),
    ])


def taskkill_f_im(name: str) -> None:
    from os import system
    system(taskkill_f_im_gen(name))
