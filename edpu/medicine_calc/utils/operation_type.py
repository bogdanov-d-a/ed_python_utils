from __future__ import annotations
from enum import Enum, auto


class OperationType(Enum):
    RESTOCK = auto()
    CONSUME = auto()
    LOSE = auto()
