from __future__ import annotations
from ..data.data import Data
from typing import Generic, TypeVar


T = TypeVar('T')


class Account(Generic[T]):
    def __init__(self: Account[T], name: str, actions: Data[T]) -> None:
        self._name = name
        self._actions = actions
        self._value = self._actions.zero()


    def get_name(self: Account[T]) -> str:
        return self._name


    def get_balance(self: Account[T]) -> str:
        return self._actions.to_string(self._value)


    def income(self: Account[T], amount: str) -> None:
        self._value = self._actions.sum(self._value, self._actions.parse(amount))


    def expense(self: Account[T], amount: str) -> None:
        self._value = self._actions.sum(self._value, self._actions.negate(self._actions.parse(amount)))


    def transfer_to(self: Account[T], target: Account[T], amount: str) -> None:
        self.expense(amount)
        target.income(amount)
