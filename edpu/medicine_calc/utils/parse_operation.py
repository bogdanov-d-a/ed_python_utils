from ..operations.operation import Operation


def parse_operation(operation: tuple) -> Operation:
    from ..operations.consume import Consume
    from ..operations.lose import Lose
    from ..operations.restock import Restock
    from .mappers.operation_type_string import string_to_operation_type
    from .operation_type import OperationType

    return {
        OperationType.RESTOCK: lambda operation: Restock(operation[1], operation[2]),
        OperationType.CONSUME: lambda operation: Consume(operation[1], operation[2], operation[3], operation[4]),
        OperationType.LOSE: lambda operation: Lose(operation[1], operation[2]),
    }[string_to_operation_type(operation[0])](operation)
