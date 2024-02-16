def removeprefix(str_: str, prefix: str) -> str:
    if str_.find(prefix) == 0:
        return str_[len(prefix):]
    return str_


def removesuffix(str_: str, suffix: str) -> str:
    if len(suffix) > len(str_):
        return str_
    str_suffix_pos = str_.find(suffix)
    if str_suffix_pos == len(str_) - len(suffix):
        return str_[:str_suffix_pos]
    return str_


def char_wrap(str_: str, char: str) -> str:
    return char + str_ + char


def apostrophe_wrap(str_: str) -> str:
    return char_wrap(str_, '\'')


def quotation_mark_wrap(str_: str) -> str:
    return char_wrap(str_, '"')


def backtick_wrap(str_: str) -> str:
    return char_wrap(str_, '`')


def merge_with_space(list_: list[str]) -> str:
    return ' '.join(list_)


def round_brackets_wrap(str_: str) -> str:
    return '(' + str_ + ')'


def comma_separate(list_: list[str]) -> str:
    return ','.join(list_)
