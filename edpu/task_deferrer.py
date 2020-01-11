import datetime
import operator
import codecs
import traceback
import edpu.query_window


def none_min(a, b):
    return b if a is None else min(a, b)


def get_info(state, now_date=None, hide_hint=False):
    result = ''

    if now_date is None:
        now_date_ = datetime.datetime.now().date()
        now_date = (now_date_.year, now_date_.month, now_date_.day)

    earliest_date = None

    for name, date_ in sorted(state, key=operator.itemgetter(1)):
        if date_ <= now_date:
            result += name + '\n'
        else:
            earliest_date = none_min(earliest_date, date_)

    if not hide_hint:
        result += 'Earliest date: ' + str(earliest_date) + '\n'

    return result


def eval_file(filename):
    with codecs.open(filename, 'r', 'utf-8') as file:
        return eval(file.read())


def get_info_from_file(state_filename, now_date=None, hide_hint=False):
    return get_info(eval_file(state_filename), now_date, hide_hint)


def info_viewer(state_filename, now_date=None, window_title='info_viewer'):
    def data_provider():
        try:
            return get_info_from_file(state_filename, now_date)
        except:
            return traceback.format_exc()
    edpu.query_window.run(data_provider, window_title)


def get_info_2d(columns, state, now_date=None):
    result = ''

    if now_date is None:
        now_date_ = datetime.datetime.now().date()
        now_date = (now_date_.year, now_date_.month, now_date_.day)

    earliest_date = None

    for name, dates in state:
        if len(columns) != len(dates):
            raise Exception("Incorrect dates count for " + name)
        for date_index in range(len(columns)):
            if dates[date_index] is not None:
                if dates[date_index] <= now_date:
                    result += name + ' - ' + columns[date_index] + ' (' + str(date_index + 1) + ')\n'
                else:
                    earliest_date = none_min(earliest_date, dates[date_index])

    result += 'Earliest date: ' + str(earliest_date) + '\n'

    return result


def get_info_2d_from_file(data_filename, now_date=None):
    data = eval_file(data_filename)
    return get_info_2d(data[0], data[1], now_date)


def info_2d_viewer(data_filename, now_date=None, window_title='info_2d_viewer'):
    def data_provider():
        try:
            return get_info_2d_from_file(data_filename, now_date)
        except:
            return traceback.format_exc()
    edpu.query_window.run(data_provider, window_title)
