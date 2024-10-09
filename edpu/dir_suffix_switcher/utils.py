from typing import Any, TypeVar


T = TypeVar('T')


def is_same_list(list_: list[Any]) -> bool:
    if len(list_) == 0:
        raise Exception('empty list is not allowed')

    for i in range(len(list_) - 1):
        if (list_[i] != list_[i + 1]):
            return False

    return True


def get_same_list_value(list_: list[T]) -> T:
    if not is_same_list(list_):
        raise Exception('not is_same_list(list_)')

    return list_[0]


def get_suffix_exists(suffix_paths: dict[str, list[str]]) -> dict[str, bool]:
    from os.path import isdir

    return {
        suffix: get_same_list_value(list(map(isdir, paths)))
        for suffix, paths in suffix_paths.items()
    }


def get_false_key(dict_: dict[str, bool]) -> str:
    from typing import Optional

    result: Optional[str] = None

    for key, value in dict_.items():
        if not value:
            if result is not None:
                raise Exception('result is not None')
            result = key

    if result is None:
        raise Exception('result is None')

    return result
