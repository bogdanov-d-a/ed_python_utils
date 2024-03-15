from enum import Enum, auto
from typing import Optional


class Type(Enum):
    SD = auto()
    NVME = auto()


def _dev(type: Type, index: str, nvme_index: Optional[str]) -> str:
    if type == Type.SD:
        return f'sd{index}'

    elif type == Type.NVME:
        if nvme_index is None:
            raise Exception()

        return f'nvme{index}n{nvme_index}'

    else:
        raise Exception()


def _part(type: Type, index: str) -> str:
    if type == Type.SD:
        return index

    elif type == Type.NVME:
        return f'p{index}'

    else:
        raise Exception()


def get(type: Type, index: str, nvme_index: Optional[str], part_index: Optional[str], add_dev: bool) -> str:
    result = _dev(type, index, nvme_index)

    if part_index is not None:
        result += _part(type, part_index)

    if add_dev:
        result = '/dev/' + result

    return result
