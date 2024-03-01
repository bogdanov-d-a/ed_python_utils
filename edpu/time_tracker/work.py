import math
from .common import *
from edpu import query_window
from edpu import file_utils
from edpu import calc_time_utils as CTU

def sorted_dict_keys(dict_):
    return sorted(dict_.keys())

def next_weekday(weekday):
    return (weekday + 1) % 7

def weekday_to_string(weekday):
    dict_ = {
        0: 'Mon',
        1: 'Tue',
        2: 'Wed',
        3: 'Thu',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun',
    }
    return dict_[weekday]

def get_left_time(rbs, annotation, day_limit, today,
                    remaining_days_range, goal_times, mock_time):
    result = ''

    if len(goal_times) == 0:
        fail()

    sum_ = 0
    for num, data in key_sorted_dict_items(rbs):
        if num >= day_limit:
            continue
        sum_ += data.total_time()
    sum_ += mock_time

    remaining_times = []
    for goal_time in goal_times:
        remaining_times.append(CTU.parse_duration(goal_time) - sum_)

    remaining_times_str = ''
    first = True
    for remaining_time in remaining_times:
        if not first:
            remaining_times_str += ' / '
        remaining_times_str += CTU.duration_string_with_negative(remaining_time)
        first = False

    result += annotation + ': ' + remaining_times_str + ' remaining for this month\n'
    worked_today = rbs[today].total_time() if today in rbs else 0

    for remaining_days in remaining_days_range:
        result += 'Average work time for ' + str(remaining_days) + ' days: '

        first = True
        for remaining_time in remaining_times:
            if not first:
                result += ' / '

            average_day_time = math.ceil(remaining_time / remaining_days)
            result += CTU.duration_string_with_negative(average_day_time)

            if worked_today != 0:
                left_today = average_day_time - worked_today
                result += ' (' + CTU.duration_string_with_negative(left_today) + ' left)'

            first = False

        result += '\n'

    return result

def get_stats(days, today, goal_times, remaining_days_range,
               remaining_days_range_next, today_work_plan, schedule_info):
    result = ''

    rbs = {}
    for day, data in key_sorted_dict_items(days):
        rb = ReportBuilder3()
        for elem in data:
            apply_action(rb, elem)
        rbs[day] = rb

    warnings = []
    for day, data in key_sorted_dict_items(rbs):
        for warning in data.get_warnings():
            warnings.append('Day ' + str(day) + ' warning: ' + warning)

    if len(warnings) > 0:
        for warning in warnings:
            result += warning + '\n'
        result += '\n'

    result += rbs[today].get_summary() if today in rbs else 'No work today\n'
    result += '\n'

    month_time = 0
    for _, data in key_sorted_dict_items(rbs):
        month_time += data.total_time()
    result += 'Total time for month: ' + CTU.duration_string_with_negative(month_time) + ' (' + str(month_time / 60) + ')\n'

    if len(goal_times) > 0 and remaining_days_range is not None:
        result += '\n'
        result += get_left_time(rbs, 'At the ' + str(today) + ' day start',
                        today, today, remaining_days_range, goal_times, 0)

        if remaining_days_range_next is not None:
            result += '\n'
            result += get_left_time(rbs, 'Leaving now', today + 1, today + 1,
                            remaining_days_range_next, goal_times, 0)

            if today_work_plan is not None:
                result += '\n'
                result += get_left_time(rbs, 'Leaving after ' + today_work_plan,
                                today, today + 1, remaining_days_range_next,
                                goal_times, CTU.parse_duration(today_work_plan))

    if schedule_info is not None:
        result += '\n'

        schedule_days = schedule_info[0]
        schedule_first_weekday = schedule_info[1]

        if sorted_dict_keys(schedule_days) != list(range(1, len(schedule_days) + 1)):
            fail()

        cur_weekday = schedule_first_weekday
        for day, data in key_sorted_dict_items(schedule_days):
            if day == today:
                result += '> '

            result += 'Day ' + str(day) + ' (' + weekday_to_string(cur_weekday) + '): ' + data[0]

            if day in rbs:
                result += ' -> ' + CTU.duration_string_with_negative(rbs[day].total_time())
                over_time = rbs[day].total_time() - CTU.parse_duration(schedule_days[day][0])
                result += ' ' + CTU.duration_string_with_negative(over_time, True)

            if len(data[1]) > 0:
                result += ' (note: ' + data[1] + ')'

            result += '\n'
            cur_weekday = next_weekday(cur_weekday)

        est_month_time_passed = 0
        real_month_time_passed = 0
        month_time_left = 0

        for day in range(1, len(schedule_days) + 1):
            if (day < today) and (day in rbs):
                real_month_time_passed += rbs[day].total_time()
                est_month_time_passed += CTU.parse_duration(schedule_days[day][0])
            else:
                month_time_left += CTU.parse_duration(schedule_days[day][0])

        est_month_time_total = est_month_time_passed + month_time_left
        real_month_time_total = real_month_time_passed + month_time_left

        est_month_time_passed_with_today = est_month_time_passed
        real_month_time_passed_with_today = real_month_time_passed
        real_month_time_total_with_today = real_month_time_total

        if today in rbs:
            real_month_time_passed_with_today += rbs[today].total_time()
            est_month_time_passed_with_today += CTU.parse_duration(schedule_days[today][0])
            real_month_time_total_with_today += rbs[today].total_time() - CTU.parse_duration(schedule_days[today][0])

        month_time_diff = real_month_time_passed - est_month_time_passed
        month_time_diff_with_today = real_month_time_passed_with_today - est_month_time_passed_with_today

        result += 'Estimation month time: '
        result += CTU.duration_string(est_month_time_total) + ' -> ' + CTU.duration_string_with_negative(real_month_time_total)
        result += ' / ' + CTU.duration_string(est_month_time_passed) + ' -> ' + CTU.duration_string_with_negative(real_month_time_passed)
        result += ' ' + CTU.duration_string_with_negative(month_time_diff, True)
        result += '\n'

        if today in rbs:
            result += 'Estimation month time (with today): '
            result += CTU.duration_string(est_month_time_total) + ' -> ' + CTU.duration_string_with_negative(real_month_time_total_with_today)
            result += ' / ' + CTU.duration_string(est_month_time_passed_with_today) + ' -> ' + CTU.duration_string_with_negative(real_month_time_passed_with_today)
            result += ' ' + CTU.duration_string_with_negative(month_time_diff_with_today, True)
            result += '\n'

        if est_month_time_passed != 0:
            real_est_ratio = real_month_time_passed / est_month_time_passed
            result += 'Estimation-start ratio: ' + str(real_est_ratio) + '\n'
            result += 'Progressive estimation: ' + CTU.duration_string(math.ceil(est_month_time_total * real_est_ratio)) + '\n'

        if today in rbs:
            if est_month_time_passed_with_today != 0:
                real_est_ratio_with_today = real_month_time_passed_with_today / est_month_time_passed_with_today
                result += 'Estimation-start ratio (with today): ' + str(real_est_ratio_with_today) + '\n'
                result += 'Progressive estimation (with today): ' + CTU.duration_string(math.ceil(est_month_time_total * real_est_ratio_with_today)) + '\n'

    return result

def stats_viewer(data_filename, goal_times, remaining_days_range,
               remaining_days_range_next, today_work_plan, schedule_info):
    def data_provider():
        data = file_utils.eval_file(data_filename)
        return get_stats(data[0], data[1], goal_times, remaining_days_range,
            remaining_days_range_next, today_work_plan, schedule_info)
    query_window.run_with_exception_wrapper(data_provider, 'Work time stats')
