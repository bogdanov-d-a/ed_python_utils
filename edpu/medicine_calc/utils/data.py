from __future__ import annotations
from typing import Any


REPORT_FILE = 'report_file'
PC_WEIGHT = 'pc_weight'
PC_PRECISION = 'pc_precision'
WEIGHT_UNIT = 'weight_unit'
OPERATIONS = 'operations'


class Data:
    def __init__(self: Data, data: dict[str, Any]) -> None:
        from .parse_operation import parse_operation

        self.report_file: str = data[REPORT_FILE]
        self.pc_weight: float = data[PC_WEIGHT]
        self.pc_precision: int = data[PC_PRECISION]
        self.weight_unit: str = data[WEIGHT_UNIT]
        self.operations = list(map(parse_operation, data[OPERATIONS]))
