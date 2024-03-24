from __future__ import annotations
from ..utils.operation_type import OperationType
from .operation import Operation


class Restock(Operation):
    def __init__(self: Restock, pcs: int, time: str) -> None:
        self.pcs = pcs
        self.time = time


    def get_type(self: Operation) -> OperationType:
        return OperationType.RESTOCK
