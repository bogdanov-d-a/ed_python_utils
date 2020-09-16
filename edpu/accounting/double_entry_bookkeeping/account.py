class Account:
    def __init__(self, name, actions):
        self._name = name
        self._actions = actions
        self._value = self._actions.zero()

    def get_name(self):
        return self._name

    def get_balance(self):
        return self._actions.to_string(self._value)

    def income(self, amount):
        self._value = self._actions.sum(self._value, self._actions.parse(amount))

    def expense(self, amount):
        self._value = self._actions.sum(self._value, self._actions.negate(self._actions.parse(amount)))

    def transfer_to(self, target, amount):
        self.expense(amount)
        target.income(amount)
