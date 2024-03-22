def powershell() -> str:
    return 'powershell.exe'


def powershell_escape_command(str_: str) -> str:
    from .string_utils import quotation_mark_wrap
    return quotation_mark_wrap(str_.replace('"', '""'))


def powershell_command(command: str) -> str:
    from .string_utils import merge_with_space

    return merge_with_space([
        powershell(),
        '-command',
        powershell_escape_command(command),
    ])
