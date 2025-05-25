class Player:
    def __init__(self, name, chips=100, is_bot=False):
        self.name = name
        self.chips = chips
        self.hand = []
        self.is_bot = is_bot

    def call(self, to_call, pot):
        amount = min(to_call, self.chips)
        self.chips -= amount
        pot += amount
        print(f"{self.name} calls {amount}. Remaining chips: {self.chips}")
        return amount, pot

    def all_in(self, pot):
        amount = self.chips
        self.chips = 0
        pot += amount
        print(f"{self.name} goes all-in with {amount}!")
        return amount, pot

    def bet_or_raise(self, current_bet, pot, amount=None, percentage=None):
        if percentage is not None:
            amount = int(min(self.chips, max(current_bet, pot * percentage)))
        else:
            amount = min(amount, self.chips)

        self.chips -= amount
        pot += amount
        print(f"{self.name} raises {amount} chips. Remaining chips: {self.chips}")
        return amount, pot

    def check(self):
        print(f"{self.name} checks.")

    def fold(self, opponent, pot):
        print(f"{self.name} folds. {opponent.name} wins the pot of {pot} chips!")
        opponent.chips += pot
        return pot, 'ended'
