def tab_string(s: str, count: int) -> str:
    return ' ' * 4 * count + s


def tab_string_list(string_list: list[str], count: int) -> list[str]:
    return list(map(
        lambda s: tab_string(s, count),
        string_list
    ))


def append_comma_string(s: str) -> str:
    return s + ','


def append_comma_string_list(string_list: list[str]) -> list[str]:
    return list(map(
        append_comma_string,
        string_list
    ))


def get_list_lines(items: list[str]) -> list[str]:
    return ['['] + tab_string_list(append_comma_string_list(items), 1) + [']']


def get_raw_string(s: str) -> str:
    from edpu.string_utils import apostrophe_wrap
    return 'r' + apostrophe_wrap(s)


def get_raw_string_list(string_list: list[str]) -> list[str]:
    return list(map(
        get_raw_string,
        string_list
    ))


def get_list_lines_of_raw_strings(string_list: list[str]) -> list[str]:
    return get_list_lines(get_raw_string_list(string_list))


def append_comma_at_last(string_list: list[str]) -> list[str]:
    return string_list[:-1] + [append_comma_string(string_list[-1])]


def append_comma_at_last_except_last(string_list_list: list[list[str]]) -> list[list[str]]:
    return list(map(
        append_comma_at_last,
        string_list_list[:-1]
    )) + [string_list_list[-1]]


def aggregate_string_list_list(string_list_list: list[list[str]]) -> list[str]:
    result = []

    for string_list in string_list_list:
        result += string_list

    return result
