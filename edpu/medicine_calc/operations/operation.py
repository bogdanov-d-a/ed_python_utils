from __future__ import annotations
from ..utils.operation_type import OperationType
from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def get_type(self: Operation) -> OperationType:
        pass
