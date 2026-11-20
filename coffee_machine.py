class NotEnoughMilk(Exception):
    pass


class CoffeeMachine:
    CAPPUCCINO_MILK = 100  # мл

    def __init__(self, milk):
        self.milk = milk

    def make_cappuccino(self):
        if self.milk < self.CAPPUCCINO_MILK:
            raise NotEnoughMilk("Недостаточно молока")
        self.milk -= self.CAPPUCCINO_MILK
        return "cappuccino"
