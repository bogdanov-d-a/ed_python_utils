import codecs
import edpu.datetime_utils

def make_report(data, report_filename):
    with codecs.open(report_filename, 'w', 'utf-8') as report_file:
        report_file.write('Created at: ' + edpu.datetime_utils.get_now_datetime_str() + '\n')
        report_file.write(data)

def make_reports(names, report_processor, src_path_provider=lambda n: n + '.py',
                 dst_path_provider=lambda n: n + '_report.txt'):
    for name in names:
        src_path = src_path_provider(name)
        dst_path = dst_path_provider(name)

        report_data = report_processor(src_path)
        make_report(report_data, dst_path)
