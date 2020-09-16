def fail():
    raise Exception('fail')

def get_info(items, data_op, subject_area):
    balance_name, income_name, expenses_name = subject_area

    result = ''
    income_sum = data_op.zero()
    expenses_sum = data_op.zero()

    for item in items:
        action = item[0]
        val_str = item[1]
        val = data_op.parse(val_str)
        note = item[2]

        if action == income_name:
            income_sum = data_op.sum(income_sum, val)
        elif action == expenses_name:
            expenses_sum = data_op.sum(expenses_sum, val)
        else:
            fail()

        result += action + ' ' + val_str + ', ' + balance_name + ' = ' + \
            data_op.to_string(income_sum) + ' - ' + data_op.to_string(expenses_sum) + ' = ' + \
            data_op.to_string(data_op.sum(income_sum, data_op.negate(expenses_sum))) + \
            ' (' + note + ')' + '\n'

    return result

def get_debt_subject_area():
    return ('debt', 'give', 'take')

def get_account_subject_area():
    return ('balance', 'income', 'expenses')
