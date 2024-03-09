def get_now_date():
    from datetime import datetime
    return datetime.now().date()


def none_min(a, b):
    return b if a is None else min(a, b)


def get_info(state, now_date=None, hide_hint=False, show_future=False):
    result = ''

    if now_date is None:
        now_date_ = get_now_date()
        now_date = (now_date_.year, now_date_.month, now_date_.day)

    earliest_date = None
    future = ''

    for name, date_ in sorted(state, key=lambda e: e[1]):
        output_str = name + ' ' + str(date_) + '\n'
        if date_ <= now_date:
            result += output_str
        else:
            if show_future:
                future += output_str
            earliest_date = none_min(earliest_date, date_)

    if not hide_hint:
        result += 'Earliest date: ' + str(earliest_date) + '\n'

    result += future
    return result


def get_info_from_file(state_filename, now_date=None, hide_hint=False):
    from .file_utils import eval_file
    return get_info(eval_file(state_filename), now_date, hide_hint)


def info_viewer(state_filename, now_date=None, window_title='info_viewer'):
    from .query_window import run_with_exception_wrapper
    run_with_exception_wrapper(lambda: get_info_from_file(state_filename, now_date), window_title)


def get_info_2d(columns, state, now_date=None):
    result = ''

    if now_date is None:
        now_date_ = get_now_date()
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
    from .file_utils import eval_file

    data = eval_file(data_filename)
    return get_info_2d(data[0], data[1], now_date)


def info_2d_viewer(data_filename, now_date=None, window_title='info_2d_viewer'):
    from .query_window import run_with_exception_wrapper
    run_with_exception_wrapper(lambda: get_info_2d_from_file(data_filename, now_date), window_title)
