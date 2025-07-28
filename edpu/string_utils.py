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


def strip_crlf(str_: str) -> str:
    return str_.rstrip('\n').rstrip('\r')


def char_wrap(str_: str, char: str) -> str:
    return char + str_ + char


def apostrophe_wrap(str_: str) -> str:
    return char_wrap(str_, '\'')


def quotation_mark_wrap(str_: str) -> str:
    return char_wrap(str_, '"')


def backtick_wrap(str_: str) -> str:
    return char_wrap(str_, '`')


def percent_wrap(str_: str) -> str:
    return char_wrap(str_, '%')


def merge_with_space(list_: list[str]) -> str:
    return ' '.join(list_)


def merge_with_semicolon(list_: list[str]) -> str:
    return ';'.join(list_)


def merge_with_newline(list_: list[str]) -> str:
    return '\n'.join(list_)


def round_brackets_wrap(str_: str) -> str:
    return '(' + str_ + ')'


def square_brackets_wrap(str_: str) -> str:
    return '[' + str_ + ']'


def curly_brackets_wrap(str_: str) -> str:
    return '{' + str_ + '}'


def angle_brackets_wrap(str_: str) -> str:
    return '<' + str_ + '>'


def comma_separate(list_: list[str]) -> str:
    return ','.join(list_)


def accent_str(lines: list[str], char: str='@') -> list[str]:
    if len(char) != 1:
        raise Exception('len(char) != 1')

    if len(lines) == 0:
        raise Exception('len(lines) == 0')

    result: list[str] = []

    max_len = max(map(
        len,
        lines
    ))

    def edge() -> None:
        result.append(char * (max_len + 4))

    edge()

    for line in lines:
        result.append(f'{char} {line}{" " * (max_len - len(line))} {char}')

    edge()

    return result


def gen_ascii_str() -> str:
    result = ''

    for byte in range(32, 127):
        result += byte.to_bytes().decode('ascii')

    return result
