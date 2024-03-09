from __future__ import annotations
from .data.data import Data
from typing import TypeVar


Item = tuple[str, str, str]
Items = list[Item]


class SubjectArea:
    def __init__(self: SubjectArea, balance: str, income: str, expenses: str) -> None:
        self.balance = balance
        self.income = income
        self.expenses = expenses


T = TypeVar('T')


def get_info(items: Items, data_op: Data[T], subject_area: SubjectArea) -> str:
    result = ''
    income_sum = data_op.zero()
    expenses_sum = data_op.zero()

    for item in items:
        action = item[0]
        val_str = item[1]
        val = data_op.parse(val_str)
        note = item[2]

        if action == subject_area.income:
            income_sum = data_op.sum(income_sum, val)
        elif action == subject_area.expenses:
            expenses_sum = data_op.sum(expenses_sum, val)
        else:
            raise Exception()

        result += action + ' ' + val_str + ', ' + subject_area.balance + ' = ' + \
            data_op.to_string(income_sum) + ' - ' + data_op.to_string(expenses_sum) + ' = ' + \
            data_op.to_string(data_op.sum(income_sum, data_op.negate(expenses_sum))) + \
            ' (' + note + ')' + '\n'

    return result


def get_debt_subject_area() -> SubjectArea:
    return SubjectArea('debt', 'give', 'take')


def get_account_subject_area() -> SubjectArea:
    return SubjectArea('balance', 'income', 'expenses')
