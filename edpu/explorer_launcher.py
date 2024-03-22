def open_dir_in_explorer(dir: str) -> None:
    from .powershell import powershell_command
    from .string_utils import merge_with_space, quotation_mark_wrap
    from os import system
    from os.path import isdir

    if not isdir(dir):
        raise Exception()

    system(powershell_command(merge_with_space([
        'Invoke-Item',
        quotation_mark_wrap(dir),
    ])))
