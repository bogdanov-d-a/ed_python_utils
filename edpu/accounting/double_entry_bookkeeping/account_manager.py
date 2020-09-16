from .log_account import *
from ..data.decimal import DecimalData


class AccountManager:
    def __init__(self, logger_factory):
        self._accounts = []
        self._logger_factory = logger_factory

    def add_account(self, name):
        if self.get_account(name) is not None:
            raise Exception()
        logger = self._logger_factory(name)
        account = LogAccount(name, DecimalData, logger)
        self._accounts.append(account)

    def get_account(self, name):
        try:
            return next(account for account in self._accounts if account.get_name() == name)
        except:
            return None

    def transfer(self, source_name, target_name, amount):
        if source_name == target_name:
            raise Exception()
        self.get_account(source_name).transfer_to(self.get_account(target_name), amount)
