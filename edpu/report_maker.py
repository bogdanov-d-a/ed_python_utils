import codecs
from typing import Callable
from . import datetime_utils

def make_report(data: str, report_filename: str) -> None:
    with codecs.open(report_filename, 'w', 'utf-8') as report_file:
        report_file.write('Created at: ' + datetime_utils.get_now_datetime_str() + '\n')
        report_file.write(data)

def make_reports(names: list[str], report_processor: Callable[[str], str], src_path_provider: Callable[[str], str]=lambda n: n + '.py',
                 dst_path_provider: Callable[[str], str]=lambda n: n + '_report.txt'):
    for name in names:
        src_path = src_path_provider(name)
        dst_path = dst_path_provider(name)

        report_data = report_processor(src_path)
        make_report(report_data, dst_path)
