from subprocess import CompletedProcess


POWERSHELL = 'powershell'
POWERSHELL_COMMAND = '-command'

POWERSHELL_EQUAL_SET = '-eq'
POWERSHELL_FOREACH = 'foreach'
POWERSHELL_IN = 'in'

POWERSHELL_INVOKE_ITEM = 'Invoke-Item'
POWERSHELL_WHERE_OBJECT = 'Where-Object'
POWERSHELL_WRITE_HOST = 'Write-Host'


def powershell_foreach(item: str, collection: str, statements: str) -> str:
    from .string_utils import merge_with_space, round_brackets_wrap, curly_brackets_wrap

    return merge_with_space([
        POWERSHELL_FOREACH,
        round_brackets_wrap(merge_with_space([
            item,
            POWERSHELL_IN,
            collection,
        ])),
        curly_brackets_wrap(statements),
    ])


def powershell_where_object(property: str, operator: str, value: str) -> str:
    from .string_utils import merge_with_space, curly_brackets_wrap

    return merge_with_space([
        POWERSHELL_WHERE_OBJECT,
        curly_brackets_wrap(merge_with_space([
            property,
            operator,
            value,
        ])),
    ])


def escape_powershell_apostrophe(s: str) -> str:
    from .escaping import escape_with_char_double
    return escape_with_char_double(s, "'")


def escape_powershell_quotation_mark(s: str) -> str:
    from .escaping import translate

    return translate(s, {
        '"': '`"',
        '`': '``',
        '$': '`$',
    })


def powershell_command(command: str) -> CompletedProcess[bytes]:
    from subprocess import run

    return run([
        POWERSHELL,
        POWERSHELL_COMMAND,
        command,
    ])
