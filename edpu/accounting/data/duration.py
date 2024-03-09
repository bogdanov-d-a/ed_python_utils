from .data import Data


class DurationData(Data[int]):
    @classmethod
    def zero(cls) -> int:
        return 0


    @classmethod
    def negate(cls, value: int) -> int:
        return -value


    @classmethod
    def sum(cls, value1: int, value2: int) -> int:
        return value1 + value2


    @classmethod
    def parse(cls, str_: str) -> int:
        from ...calc_time_utils import parse_duration
        return parse_duration(str_)


    @classmethod
    def to_string(cls, value: int) -> str:
        from ...calc_time_utils import duration_string_with_negative
        return duration_string_with_negative(value)
