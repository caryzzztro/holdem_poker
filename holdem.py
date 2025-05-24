from deck import Card, Deck
from collections import Counter
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♣', '♦']
RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
               '7': 7, '8': 8, '9': 9, 'T': 10,
               'J': 11, 'Q': 12, 'K': 13, 'A': 14}
SUIT_VALUES = {'♠': 4, '♥': 3, '♦': 2, '♣': 1}

# rank the value of list for the hand from high to low
def rank_value_list(ranks):
    return sorted(ranks, key=lambda r: RANK_VALUES[r], reverse=True)

# get the group of rank, sort by the frequency of the rank, if the frequency is the same, sort by the rank
def get_rank_groups(hand):
    ranks = [card.rank for card in hand]
    freq = {}
    for r in ranks:
        freq[r] = freq.get(r, 0) + 1

    # Group by frequency: {count -> list of ranks with that count}
    grouped = {}
    for rank, count in freq.items():
        if count not in grouped:
            grouped[count] = []
        grouped[count].append(rank)

    return grouped  # e.g., {3: ['K'], 2: ['T']} for a full house

# get the suit of the hand group
def get_suit_groups(hand):
    suits = {}
    for card in hand:
        suits.setdefault(card.suit, []).append(card)
    return suits

# determine the card types
def is_full_house(hand):
    groups = get_rank_groups(hand)

    if 3 in groups and 2 in groups:
        three = groups[3][0]
        pair = groups[2][0]
        return True, [three] * 3 + [pair] * 2
    return False, []

def is_flush(hand):
    suits = [card.suit for card in hand]
    for suit in SUITS:
        if suits.count(suit) == 5:
            # Return cards in descending rank order
            flush_ranks = sorted(
                [card.rank for card in hand if card.suit == suit],
                key=lambda r: RANK_VALUES[r],
                reverse=True
            )
            return True, flush_ranks
    return False, []

def is_straight(hand):
    values = sorted(set(card.value for card in hand))

    # Handle A-2-3-4-5 (wheel)
    if values == [2, 3, 4, 5, 14]:
        return True, ['5', '4', '3', '2', 'A']

    # Normal straight
    if len(values) == 5 and values[-1] - values[0] == 4:
        sorted_ranks = sorted([card.rank for card in hand], key=lambda r: RANK_VALUES[r])
        return True, sorted_ranks
    return False, []

def is_three_of_a_kind(hand):
    groups = get_rank_groups(hand)
    if 3 in groups and len(groups) == 3:  # one 3-of-a-kind and two kickers
        three = groups[3][0]
        kickers = rank_value_list([r for r in groups.get(1, [])])
        return True, [three] * 3 + kickers
    return False, []

def is_two_pair(hand):
    groups = get_rank_groups(hand)
    if 2 in groups and len(groups[2]) == 2:
        pairs = sorted(groups[2], key=lambda r: RANK_VALUES[r], reverse=True)
        kicker = [r for r in groups.get(1, [])][0]
        return True, [pairs[0]] * 2 + [pairs[1]] * 2 + [kicker]
    return False, []

def is_one_pair(hand):
    groups = get_rank_groups(hand)
    if 2 in groups and len(groups[2]) == 1:
        pair = groups[2][0]
        kickers = rank_value_list([r for r in groups.get(1, [])])
        return True, [pair] * 2 + kickers
    return False, []

def is_high_card(hand):
    ranks = [card.rank for card in hand]
    sorted_ranks = rank_value_list(ranks)
    return True, sorted_ranks

def is_four_of_a_kind(hand):
    groups = get_rank_groups(hand)
    if 4 in groups:
        quad = groups[4][0]
        kicker = [r for r in groups.get(1, [])][0]
        return True, [quad] * 4 + [kicker]
    return False, []
def is_straight_flush(hand):
    is_s, straight_vals = is_straight(hand)
    is_f, flush_vals = is_flush(hand)

    if is_s and is_f:
        return True, straight_vals  # ascending, as you wanted
    return False, []

HAND_RANKINGS = [
    ('Straight Flush', is_straight_flush),
    ('Four of a Kind', is_four_of_a_kind),
    ('Full House', is_full_house),
    ('Flush', is_flush),
    ('Straight', is_straight),
    ('Three of a Kind', is_three_of_a_kind),
    ('Two Pair', is_two_pair),
    ('One Pair', is_one_pair),
    ('High Card', is_high_card),
]
# implement the classify function to return the highest type of hand for the 5 card of hand(high to low), if the
# cardtype is true return true and the hand of the card
def classify_hand(hand):
    for name, func in HAND_RANKINGS:
        cardtype, ranks = func(hand)
        if cardtype:
            return name, ranks
    return "Unknown", []

# test section
if __name__ == '__main__':
    pass
    # # a test function that test the type of the card
    # def test_random_hand():
    #     deck = Deck()
    #     hand = deck.deal(5)
    #     print("Hand:", hand)
    #
    #     hand_type, value = classify_hand(hand)
    #     print("Hand Type:", hand_type)
    #     print("Value:", value)
    #     return hand_type
    # result_lst = {}
    # # random generate 100000 times for summarise the hand
    # for _ in range(100000):
    #     print("----- New Hand -----")
    #     type = test_random_hand()
    #     if type not in result_lst:
    #         result_lst[type] = 0
    #     result_lst[type] += 1
    #
    # # summarise the hand
    # print("----- type summary -----")
    # print(result_lst)
    # def is_flush(suits)->(bool):
    #     flush = all(suit == suits[0] for suit in suits)
    #     return flush
    #
    # print(is_flush(['♠','♠','♠']))
    # print(is_flush(['♠','♠','♠','♣']))

