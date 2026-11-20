class InsufficientFunds(Exception):
    pass


class ATM:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Недостаточно средств")
        self.balance -= amount
        return amount
