import datetime
import operator
import codecs
import webbrowser

out_filename = '~tmp.txt'

def info(state, now_date=None):
    if now_date is None:
        now_date_ = datetime.datetime.now().date()
        now_date = (now_date_.year, now_date_.month, now_date_.day)

    with codecs.open(out_filename, 'w') as out_file:
        for name, date_ in sorted(state, key=operator.itemgetter(1)):
            if date_ <= now_date:
                out_file.write(name + '\n')

    webbrowser.open(out_filename)
