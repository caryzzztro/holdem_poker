class Player:
    def __init__(self, name, is_bot=False, chips=1000):
        self.name = name
        self.is_bot = is_bot
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.folded = False

    def bet(self, amount):
        amount = min(amount, self.chips)
        self.chips -= amount
        self.current_bet += amount
        return amount

    def reset_for_new_round(self):
        self.current_bet = 0
        self.folded = False
        self.hand = []

    def is_bot(self):
        return self.is_bot