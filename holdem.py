from deck import Card, Deck
class hand:
    def __init__(self,cards:[Card]):
        self.hand = sorted(cards) # sorted

    def is_straight(self)-> (bool,int): # check whether the hand is straight
        values = [card.value for card in self.hand]
        # check regular straight
        regular_straight = all(values[i] + 1 == values[i + 1] for i in range(4))
        if regular_straight:
            return True,values[-1]
        # if the hand has a, check wheel straight
        elif 14 in values:
            low_ace_values = sorted([1 if v == 14 else v for v in values])
            is_wheel_straight = all(low_ace_values[i] + 1 == low_ace_values[i + 1] for i in range(4))
        else:
            is_wheel_straight = False
        if is_wheel_straight:
            return True,5
        else:
            return False,-1

    def is_flush(self)->(bool,int): # check whether the hand is flush
        suits = [card.suit for card in self.hand]
        # if all the suits are same
        flush = all(suit == suits[0] for suit in suits)
        if flush:
            return True,self.hand[-1].get_rank()
        else:
            return False,-1

    def is_straight_flush(self)->(bool,int):
        is_straight, h_value = self.is_straight()
        is_flush, h_value = self.is_flush()
        if is_flush and is_straight:
            return True, h_value
        else:
            return False, -1

    def is_full_house(self)->(bool,int):
        values = [card.value for card in self.hand]

# test section
if __name__ == '__main__':
    # def is_flush(suits)->(bool):
    #     flush = all(suit == suits[0] for suit in suits)
    #     return flush
    #
    # print(is_flush(['♠','♠','♠']))
    # print(is_flush(['♠','♠','♠','♣']))

