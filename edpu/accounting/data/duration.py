from ... import calc_time_utils


class DurationData:
    @classmethod
    def zero(cls):
        return 0

    @classmethod
    def negate(cls, value):
        return -value

    @classmethod
    def sum(cls, value1, value2):
        return value1 + value2

    @classmethod
    def parse(cls, str_):
        return calc_time_utils.parse_duration(str_)

    @classmethod
    def to_string(cls, value):
        return calc_time_utils.duration_string_with_negative(value)
