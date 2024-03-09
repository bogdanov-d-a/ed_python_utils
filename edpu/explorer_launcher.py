def open_dir_in_explorer(dir: str) -> None:
    from .string_utils import merge_with_space, quotation_mark_wrap
    from os import system

    system(merge_with_space([
        'explorer',
        quotation_mark_wrap(dir),
    ]))
