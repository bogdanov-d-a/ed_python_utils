from decimal import *
import edpu.calc_time_utils

def fail():
    raise Exception('fail')

def get_info(items, value_def, subject_area):
    zero_val, negate_cb, add_cb, parse_cb, to_str_cb = value_def
    balance_name, income_name, expenses_name = subject_area

    result = ''
    balance = zero_val

    for item in items:
        action = item[0]
        sum_str = item[1]
        sum_ = parse_cb(sum_str)
        note = item[2]

        if action == income_name:
            balance = add_cb(balance, sum_)
        elif action == expenses_name:
            balance = add_cb(balance, negate_cb(sum_))
        else:
            fail()

        result += action + ' ' + sum_str + ', ' + balance_name + ' ' + to_str_cb(balance) + ' (' + note + ')' + '\n'

    return result

def get_decimal_value_def():
    return (Decimal(0), lambda v: -v, lambda v1, v2: v1 + v2, Decimal, str)

def get_time_value_def():
    return (0, lambda v: -v, lambda v1, v2: v1 + v2, edpu.calc_time_utils.parse_duration, edpu.calc_time_utils.duration_string_with_negative)

def get_debt_subject_area():
    return ('debt', 'give', 'take')

def get_account_subject_area():
    return ('balance', 'income', 'expenses')
