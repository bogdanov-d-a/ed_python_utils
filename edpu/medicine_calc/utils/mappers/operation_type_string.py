from ....mapper import Mapper
from ..operation_type import OperationType


def _get_mapper() -> Mapper[OperationType, str]:
    return Mapper([
        (OperationType.RESTOCK, 'restock'),
        (OperationType.CONSUME, 'consume'),
        (OperationType.LOSE, 'lose'),
    ])


_mapper = _get_mapper()


operation_type_to_string = _mapper.fwd
string_to_operation_type = _mapper.rev
