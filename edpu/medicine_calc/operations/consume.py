from __future__ import annotations
from ..utils.operation_type import OperationType
from .operation import Operation


class Consume(Operation):
    def __init__(self: Consume, pcs: int, day: str, day_part: str, time: str) -> None:
        self.pcs = pcs
        self.day = day
        self.day_part = day_part
        self.time = time


    def get_type(self: Operation) -> OperationType:
        return OperationType.CONSUME
