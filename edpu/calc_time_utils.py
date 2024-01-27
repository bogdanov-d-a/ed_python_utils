from typeguard import typechecked
from typing import NoReturn


@typechecked
def fail(msg: str='fail') -> NoReturn:
    raise Exception(msg)


@typechecked
def hm_to_m(hours: int, minutes: int) -> int:
    if hours < 0:
        fail()
    if minutes < 0:
        fail()

    return hours * 60 + minutes


@typechecked
def m_to_hm(minutes: int) -> tuple[int, int]:
    if minutes < 0:
        fail()

    return (minutes // 60, minutes % 60)


@typechecked
def validate_time(time: int) -> int:
    if time < 0:
        fail()

    return time


@typechecked
def validate_time_point(time: int) -> int:
    validate_time(time)

    if time >= 24 * 60:
        fail()

    return time


@typechecked
def parse_time_point(str_: str) -> int:
    if len(str_) != 5:
        fail(str_)
    if str_[2] != ':':
        fail(str_)

    h: int = int(str_[:2])
    m: int = int(str_[3:])

    if h >= 24 or m >= 60:
        fail(str_)

    return validate_time_point(hm_to_m(h, m))


@typechecked
def get_duration_postfix_mult(postfix: str) -> int:
    if postfix == 'm':
        return 1
    elif postfix == 'h':
        return 60
    else:
        fail(postfix + ' postfix')


@typechecked
def parse_duration(str_: str) -> int:
    result: int = 0

    for part in str_.split(' '):
        mult: int = get_duration_postfix_mult(part[-1:])
        result += mult * int(part[:-1])

    return result


@typechecked
def time_format_helper(num: int) -> str:
    if num < 0:
        fail()
    grow: int = 2 - len(str(num))
    if grow < 0:
        fail()
    return '0' * grow + str(num)


@typechecked
def time_point_string(tp: int) -> str:
    validate_time_point(tp)
    h, m = m_to_hm(tp)
    return time_format_helper(h) + ':' + time_format_helper(m)


@typechecked
def duration_string(d: int) -> str:
    h, m = m_to_hm(d)
    result: str = ''

    if h != 0:
        result += str(h) + 'h '

    result += str(m) + 'm'
    return result


@typechecked
def duration_string_with_negative(d: int, show_pos: bool=False) -> str:
    if d < 0:
        prefix = '-('
        suffix = ')'
    else:
        if show_pos:
            prefix = '+('
            suffix = ')'
        else:
            prefix = ''
            suffix = ''

    return prefix + duration_string(abs(d)) + suffix
