class Player:
    def __init__(self, name, is_bot=False, chips=1000):
        self.name = name
        self.is_bot = is_bot
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.folded = False


    def bet(self, min_bet, pot):
        while True:
            try:
                amount = int(input(f"{self.name}, enter your bet (min {min_bet}): "))
                if amount < min_bet:
                    print(f"Bet must be at least {min_bet}.")
                elif amount > self.chips:
                    print("You can't bet more than your total chips.")
                else:
                    self.chips -= amount
                    pot += amount
                    print(f"{self.name} bets {amount}. Remaining chips: {self.chips}")
                    return amount, pot
            except ValueError:
                print("Please enter a valid number.")

    def raise_bet(self, current_bet, pot):
        while True:
            try:
                amount = int(input(f"{self.name}, enter raise amount (must exceed {current_bet}): "))
                if amount <= current_bet:
                    print("Raise must be higher than the current bet.")
                elif amount > self.chips:
                    print("You can't raise more than your total chips.")
                else:
                    self.chips -= amount
                    pot += amount
                    print(f"{self.name} raises to {amount}. Remaining chips: {self.chips}")
                    return amount, pot
            except ValueError:
                print("Please enter a valid number.")

    def call(self, to_call, pot):
        if self.chips < to_call:
            print(f"{self.name} goes all-in with {self.chips} (not enough to call {to_call}).")
            all_in_amount = self.chips
            pot += all_in_amount
            self.chips = 0
            return all_in_amount, pot
        else:
            self.chips -= to_call
            pot += to_call
            print(f"{self.name} calls {to_call}. Remaining chips: {self.chips}")
            return to_call, pot

    def all_in(self, pot):
        all_in_amount = self.chips
        self.chips = 0
        pot += all_in_amount
        print(f"{self.name} goes all-in with {all_in_amount}!")
        return all_in_amount, pot