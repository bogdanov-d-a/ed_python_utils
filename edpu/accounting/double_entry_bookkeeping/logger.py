from __future__ import annotations


class Logger:
    def __init__(self: Logger, name: str) -> None:
        self.name = name
        self.data = ''


    def income(self: Logger, amount: str, balance: str) -> None:
        self.data += 'income ' + amount + ', balance ' + balance + '\n'


    def expense(self: Logger, amount: str, balance: str) -> None:
        self.data += 'expense ' + amount + ', balance ' + balance + '\n'
