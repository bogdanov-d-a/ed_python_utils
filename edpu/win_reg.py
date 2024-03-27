from typing import Any, Iterable


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
