from __future__ import annotations
from ..utils.operation_type import OperationType
from .operation import Operation


class Lose(Operation):
    def __init__(self: Lose, pcs: int, time: str) -> None:
        self.pcs = pcs
        self.time = time


    def get_type(self: Operation) -> OperationType:
        return OperationType.LOSE
