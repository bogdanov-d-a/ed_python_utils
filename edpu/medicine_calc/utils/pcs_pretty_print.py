from .data import Data


def pcs_pretty_print(pcs: int, data: Data) -> str:
    return f'{str(pcs)} pcs ({str(round(pcs * data.pc_weight, data.pc_precision))} {data.weight_unit})'
