from .account import *


class LogAccount(Account):
    def __init__(self, name, actions, logger):
        Account.__init__(self, name, actions)
        self._logger = logger

    def income(self, amount):
        Account.income(self, amount)
        self._logger.income(amount, self.get_balance())

    def expense(self, amount):
        Account.expense(self, amount)
        self._logger.expense(amount, self.get_balance())
