def open_dir_in_explorer(dir: str) -> None:
    from .powershell import POWERSHELL_INVOKE_ITEM, escape_powershell_apostrophe, powershell_command
    from .string_utils import apostrophe_wrap, merge_with_space
    from os.path import isdir

    if not isdir(dir):
        raise Exception()

    powershell_command(merge_with_space([
        POWERSHELL_INVOKE_ITEM,
        apostrophe_wrap(escape_powershell_apostrophe(dir)),
    ]))
