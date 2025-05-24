import random
import functools

# Ranks and suits
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♣', '♦']
RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
               '7': 7, '8': 8, '9': 9, 'T': 10,
               'J': 11, 'Q': 12, 'K': 13, 'A': 14}
SUIT_VALUES = {'♠': 4, '♥': 3, '♦': 2, '♣': 1}


@functools.total_ordering  # using for the card comparision instead of create all comparison function
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUES[rank]  # for comparison

    def __str__(self):
        return f"{self.suit}{self.rank}"

    def __repr__(self):
        return str(self)

    def get_rank(self) -> str:
        return self.rank

    def get_suit(self) -> str:
        return self.suit

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        if self.value != other.value:
            return self.value < other.value
        return SUIT_VALUES[self.suit] < SUIT_VALUES[other.suit]


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num=1):
        return [self.cards.pop() for _ in range(num)]

    def compare_cards(self, card1, card2):
        val1 = RANK_VALUES[card1.rank]
        val2 = RANK_VALUES[card2.rank]

        if val1 > val2:
            return 1
        elif val1 < val2:
            return -1
        else:
            suit1 = SUIT_VALUES[card1.suit]
            suit2 = SUIT_VALUES[card2.suit]
            if suit1 > suit2:
                return 1
            elif suit1 < suit2:
                return -1
            else:
                return 0

# test
if __name__ == '__main__':
    deck = Deck()
    hand = deck.deal(5)
    sorted_hand = sorted(hand)
    print('original', hand)
    print('sorted', sorted_hand)
