class Logger:
    def __init__(self, name):
        self.name = name
        self.data = ''

    def income(self, amount, balance):
        self.data += 'income ' + amount + ', balance ' + balance + '\n'

    def expense(self, amount, balance):
        self.data += 'expense ' + amount + ', balance ' + balance + '\n'
