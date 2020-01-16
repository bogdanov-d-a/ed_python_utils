from decimal import *
import edpu.calc_time_utils

def fail():
    raise Exception('fail')

def get_info(items, zero_val, negate_cb, add_cb, parse_cb, to_str_cb):
    result = ''
    debt = zero_val

    for item in items:
        action = item[0]
        sum_str = item[1]
        sum_ = parse_cb(sum_str)
        note = item[2]

        if action == 'give':
            debt = add_cb(debt, sum_)
        elif action == 'take':
            debt = add_cb(debt, negate_cb(sum_))
        else:
            fail()

        result += action + ' ' + sum_str + ', debt ' + to_str_cb(debt) + ' (' + note + ')' + '\n'

    return result

def get_info_decimal(items):
    return get_info(items, Decimal(0), lambda v: -v, lambda v1, v2: v1 + v2, Decimal, str)

def get_info_time(items):
    return get_info(items, 0, lambda v: -v, lambda v1, v2: v1 + v2, edpu.calc_time_utils.parse_duration, edpu.calc_time_utils.duration_string_with_negative)
