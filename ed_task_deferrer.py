import datetime
import operator
import codecs
import webbrowser

out_filename = '~tmp.txt'

def none_min(a, b):
    return b if a is None else min(a, b)

def info(state, now_date=None):
    if now_date is None:
        now_date_ = datetime.datetime.now().date()
        now_date = (now_date_.year, now_date_.month, now_date_.day)

    earliest_date = None

    with codecs.open(out_filename, 'w') as out_file:
        for name, date_ in sorted(state, key=operator.itemgetter(1)):
            if date_ <= now_date:
                out_file.write(name + '\n')
            else:
                earliest_date = none_min(earliest_date, date_)

        out_file.write('Earliest date: ' + str(earliest_date) + '\n')

    webbrowser.open(out_filename)

def info_2d(columns, state, now_date=None):
    if now_date is None:
        now_date_ = datetime.datetime.now().date()
        now_date = (now_date_.year, now_date_.month, now_date_.day)

    earliest_date = None

    with codecs.open(out_filename, 'w') as out_file:
        for name, dates in state:
            if len(columns) != len(dates):
                raise Exception("Incorrect dates count for " + name)
            for date_index in range(len(columns)):
                if dates[date_index] is not None:
                    if dates[date_index] <= now_date:
                        out_file.write(name + ' - ' + columns[date_index] + '\n')
                    else:
                        earliest_date = none_min(earliest_date, dates[date_index])

        out_file.write('Earliest date: ' + str(earliest_date) + '\n')

    webbrowser.open(out_filename)