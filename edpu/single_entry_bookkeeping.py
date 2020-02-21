from decimal import *
import edpu.calc_time_utils

def fail():
    raise Exception('fail')

def get_info(items, value_def, subject_area):
    zero_val, negate_cb, add_cb, parse_cb, to_str_cb = value_def
    balance_name, income_name, expenses_name = subject_area

    result = ''
    income_sum = zero_val
    expenses_sum = zero_val

    for item in items:
        action = item[0]
        val_str = item[1]
        val = parse_cb(val_str)
        note = item[2]

        if action == income_name:
            income_sum = add_cb(income_sum, val)
        elif action == expenses_name:
            expenses_sum = add_cb(expenses_sum, val)
        else:
            fail()

        result += action + ' ' + val_str + ', ' + balance_name + ' = ' + \
            to_str_cb(income_sum) + ' - ' + to_str_cb(expenses_sum) + ' = ' + \
            to_str_cb(add_cb(income_sum, negate_cb(expenses_sum))) + \
            ' (' + note + ')' + '\n'

    return result

def get_decimal_value_def():
    return (Decimal(0), lambda v: -v, lambda v1, v2: v1 + v2, Decimal, str)

def get_time_value_def():
    return (0, lambda v: -v, lambda v1, v2: v1 + v2, edpu.calc_time_utils.parse_duration, edpu.calc_time_utils.duration_string_with_negative)

def get_debt_subject_area():
    return ('debt', 'give', 'take')

def get_account_subject_area():
    return ('balance', 'income', 'expenses')
