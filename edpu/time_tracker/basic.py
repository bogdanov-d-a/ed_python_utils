from .common import *
from edpu import query_window
from edpu import file_utils

def get_stats(actions):
    result = ''

    rb = ReportBuilder3()
    for action in actions:
        apply_action(rb, action)

    warnings = rb.get_warnings()
    if len(warnings) > 0:
        for warning in warnings:
            result += warning + '\n'
        result += '\n'

    result += rb.get_summary()

    return result

def stats_viewer(data_filename):
    def data_provider():
        data = file_utils.eval_file(data_filename)
        return get_stats(data[0][data[1]])
    query_window.run_with_exception_wrapper(data_provider, 'Time stats')
