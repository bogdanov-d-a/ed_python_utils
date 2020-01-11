from decimal import *

def fail():
    raise Exception('fail')

def get_info(items):
    result = ''
    debt = Decimal(0)

    for item in items:
        action = item[0]
        sum_str = item[1]
        sum_ = Decimal(sum_str)
        note = item[2]

        if action == 'give':
            debt += sum_
        elif action == 'take':
            debt -= sum_
        else:
            fail()

        result += action + ' ' + sum_str + ', debt ' + str(debt) + ' (' + note + ')' + '\n'

    return result

def trace(items):
    print(get_info(items))
