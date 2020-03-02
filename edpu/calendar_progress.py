import datetime
import math

def fail(msg='fail'):
    raise Exception(msg)

def get_progress_matrix(progress, capacity, columns):
    result = ''

    if capacity <= 0:
        fail()

    remaining = capacity - progress
    if remaining < 0:
        fail()

    rows = math.ceil(capacity / columns)

    blank = rows * columns - capacity
    if blank < 0:
        fail()

    for row in range(rows):
        for column in range(columns):
            if progress > 0:
                progress -= 1
                result += 'X'
            elif remaining > 0:
                remaining -= 1
                result += '.'
            else:
                blank -= 1
                result += ' '
        result += '\n'

    if progress != 0:
        fail()
    if remaining != 0:
        fail()
    if blank != 0:
        fail()

    return result

def get_report(cal_data, progress_matrix_columns):
    today_ = datetime.date.today()
    today = (today_.year, today_.month, today_.day)

    total_days = 0
    passed_days = 0

    for month, days in cal_data:
        total_days += days
        if month < (today[0], today[1]):
            passed_days += days
        elif month == (today[0], today[1]):
            passed_days += today[2]

    remaining_days = total_days - passed_days

    result = ''
    result += 'Today: ' + str(today) + '\n'
    result += 'Total days: ' + str(total_days) + '\n'
    result += 'Passed days: ' + str(passed_days) + ' (' + str(100 * passed_days / total_days) + '%)' + '\n'
    result += 'Remaining days: ' + str(remaining_days) + ' (' + str(100 * remaining_days / total_days) + '%)' + '\n'
    result += get_progress_matrix(passed_days, total_days, progress_matrix_columns) + '\n'
    return result
