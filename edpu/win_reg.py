from typing import Any, Iterable, Optional


REG = 'reg'
DEFAULT_ENCODING = 'utf_16_le'


def reg_delete_gen(key: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    return merge_with_space([
        REG,
        'delete',
        quotation_mark_wrap(key),
        '/f',
    ])


def reg_delete(key: str) -> None:
    from os import system
    system(reg_delete_gen(key))


def reg_export_gen(key: str, file: str, overwrite: bool=False) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    data = [
        REG,
        'export',
        quotation_mark_wrap(key),
        quotation_mark_wrap(file),
    ]

    if overwrite:
        data.append('/y')

    return merge_with_space(data)


def reg_export(key: str, file: str, overwrite: bool=False) -> None:
    from os import system
    system(reg_export_gen(key, file, overwrite))


def reg_export_and_convert(key: str, file: str, encoding: str='utf_8') -> None:
    reg_export(key, file, True)
    convert_file_encoding(file, encoding=encoding)


def convert_file_encoding(path_in: str, path_out: Optional[str]=None, encoding: str='utf_8', forward: bool=True) -> None:
    from .convert_file_encoding import convert_file_encoding as impl
    encoding_in, encoding_out = (DEFAULT_ENCODING, encoding) if forward else (encoding, DEFAULT_ENCODING)
    impl(encoding_in, encoding_out, path_in, path_out)


def enum_key(key: Any) -> Iterable[str]:
    index = 0

    while True:
        try:
            from winreg import EnumKey
            yield EnumKey(key, index)
            index += 1

        except EnvironmentError:
            break


def enum_value(key: Any) -> Iterable[tuple[str, Any, int]]:
    index = 0

    while True:
        try:
            from winreg import EnumValue
            yield EnumValue(key, index)
            index += 1

        except EnvironmentError:
            break
