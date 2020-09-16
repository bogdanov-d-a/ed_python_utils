from decimal import *


class DecimalData:
    @classmethod
    def zero(cls):
        return Decimal(0)

    @classmethod
    def negate(cls, value):
        return -value

    @classmethod
    def sum(cls, value1, value2):
        return value1 + value2

    @classmethod
    def parse(cls, str_):
        return Decimal(str_)

    @classmethod
    def to_string(cls, value):
        return str(value)
