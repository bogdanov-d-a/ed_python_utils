def fail(msg='fail'):
    raise Exception(msg)

def hm_to_m(hours, minutes):
    if type(hours) is not int:
        fail()
    if hours < 0:
        fail()
    if type(minutes) is not int:
        fail()
    if minutes < 0:
        fail()
    return hours * 60 + minutes

def m_to_hm(minutes):
    if type(minutes) is not int:
        fail()
    if minutes < 0:
        fail()
    return (int(minutes / 60), minutes % 60)

def validate_time(time):
    if type(time) is not int:
        fail()
    if time < 0:
        fail()

def validate_time_point(time):
    validate_time(time)
    if time >= 24 * 60:
        fail()

def parse_time_point(str_):
    if type(str_) is not str:
        fail()
    if len(str_) != 5:
        fail(str_)
    if str_[2] != ':':
        fail(str_)

    h = int(str_[:2])
    m = int(str_[3:])
    if h >= 24 or m >= 60:
        fail(str_)

    result = hm_to_m(int(str_[:2]), int(str_[3:]))
    validate_time_point(result)
    return result

def get_duration_postfix_mult(postfix):
    if postfix == 'm':
        return 1
    elif postfix == 'h':
        return 60
    else:
        fail(postfix + ' postfix')

def parse_duration(str_):
    result = 0
    for part in str_.split(' '):
        mult = get_duration_postfix_mult(part[-1:])
        result += mult * int(part[:-1])
    return result

def time_format_helper(num):
    if type(num) is not int:
        fail()
    if num < 0:
        fail()
    grow = 2 - len(str(num))
    if grow < 0:
        fail()
    return '0' * grow + str(num)

def time_point_string(tp):
    validate_time_point(tp)
    h, m = m_to_hm(tp)
    return time_format_helper(h) + ':' + time_format_helper(m)

def duration_string(d):
    h, m = m_to_hm(d)
    result = ''
    if h != 0:
        result += str(h) + 'h '
    result += str(m) + 'm'
    return result

def duration_string_with_negative(d, show_pos=False):
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
