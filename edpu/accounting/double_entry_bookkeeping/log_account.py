from __future__ import annotations
from ..data.data import Data
from .account import Account
from .logger import Logger
from typing import Generic, TypeVar


T = TypeVar('T')


class LogAccount(Generic[T], Account[T]):
    def __init__(self: LogAccount[T], name: str, actions: Data[T], logger: Logger) -> None:
        super().__init__(name, actions)
        self._logger = logger


    def income(self: LogAccount[T], amount: str) -> None:
        super().income(amount)
        self._logger.income(amount, self.get_balance())


    def expense(self: LogAccount[T], amount: str) -> None:
        super().expense(amount)
        self._logger.expense(amount, self.get_balance())
