from .data import Data
from decimal import Decimal


class DecimalData(Data[Decimal]):
    @classmethod
    def zero(cls) -> Decimal:
        return Decimal(0)


    @classmethod
    def negate(cls, value: Decimal) -> Decimal:
        return -value


    @classmethod
    def sum(cls, value1: Decimal, value2: Decimal) -> Decimal:
        return value1 + value2


    @classmethod
    def parse(cls, str_: str) -> Decimal:
        return Decimal(str_)


    @classmethod
    def to_string(cls, value: Decimal) -> str:
        return str(value)
