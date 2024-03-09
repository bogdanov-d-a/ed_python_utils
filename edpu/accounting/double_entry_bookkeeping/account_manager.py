from __future__ import annotations
from ..data.data import Data
from .account import Account
from .logger import Logger
from typing import Callable, Generic, Optional, TypeVar


T = TypeVar('T')


class AccountManager(Generic[T]):
    def __init__(self: AccountManager[T], actions: Data[T], logger_factory: Callable[[str], Logger]) -> None:
        self._accounts: list[Account[T]] = []
        self._actions = actions
        self._logger_factory = logger_factory


    def add_account(self: AccountManager[T], name: str) -> None:
        from .log_account import LogAccount

        if self._get_account(name) is not None:
            raise Exception()

        logger = self._logger_factory(name)
        account = LogAccount(name, self._actions, logger)
        self._accounts.append(account)


    def _get_account(self: AccountManager[T], name: str) -> Optional[Account[T]]:
        return next((account for account in self._accounts if account.get_name() == name), None)


    def get_account(self: AccountManager[T], name: str) -> Account[T]:
        result = self._get_account(name)

        if result is None:
            raise Exception()

        return result


    def transfer(self: AccountManager[T], source_name: str, target_name: str, amount: str) -> None:
        if source_name == target_name:
            raise Exception()

        self.get_account(source_name).transfer_to(self.get_account(target_name), amount)
