from deck import Card, Deck
from collections import Counter
import itertools

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♣', '♦']
RANK_VALUES = {r: i for i, r in enumerate(RANKS, 2)}

HAND_RANKINGS = [
    ('Straight Flush', lambda h: is_straight_flush(h)),
    ('Four of a Kind', lambda h: is_n_of_a_kind(h, 4)),
    ('Full House', lambda h: is_full_house(h)),
    ('Flush', lambda h: is_flush(h)),
    ('Straight', lambda h: is_straight(h)),
    ('Three of a Kind', lambda h: is_n_of_a_kind(h, 3)),
    ('Two Pair', lambda h: is_two_pair(h)),
    ('One Pair', lambda h: is_n_of_a_kind(h, 2)),
    ('High Card', lambda h: is_high_card(h))
]

def get_rank_groups(hand):
    ranks = [card.rank for card in hand]
    counter = Counter(ranks)
    grouped = {}
    for r, count in counter.items():
        grouped.setdefault(count, []).append(r)
    return grouped

def is_flush(hand):
    suits = [card.suit for card in hand]
    for suit in SUITS:
        if suits.count(suit) >= 5:
            return True, sorted([card.rank for card in hand if card.suit == suit], key=lambda r: RANK_VALUES[r], reverse=True)
    return False, []

def is_straight(hand):
    values = sorted(set(RANK_VALUES[card.rank] for card in hand))
    for i in range(len(values) - 4):
        if values[i+4] - values[i] == 4:
            return True, values[i+4]
    if set([2, 3, 4, 5, 14]).issubset(values):
        return True, 5
    return False, []

def is_straight_flush(hand):
    is_f, flush_cards = is_flush(hand)
    if not is_f:
        return False, []
    flush_hand = [card for card in hand if card.rank in flush_cards]
    return is_straight(flush_hand)

def is_full_house(hand):
    grouped = get_rank_groups(hand)
    if 3 in grouped and 2 in grouped:
        return True, grouped[3] + grouped[2]
    return False, []

def is_n_of_a_kind(hand, n):
    grouped = get_rank_groups(hand)
    if n in grouped:
        remaining = [r for r in [card.rank for card in hand] if r not in grouped[n]]
        return True, grouped[n] + sorted(remaining, key=lambda r: RANK_VALUES[r], reverse=True)
    return False, []

def is_two_pair(hand):
    grouped = get_rank_groups(hand)
    if 2 in grouped and len(grouped[2]) >= 2:
        pairs = sorted(grouped[2], key=lambda r: RANK_VALUES[r], reverse=True)
        kickers = [r for r in [card.rank for card in hand] if r not in pairs[:2]]
        return True, pairs[:2] + kickers[:1]
    return False, []

def is_high_card(hand):
    return True, sorted([card.rank for card in hand], key=lambda r: RANK_VALUES[r], reverse=True)

def classify_hand(hand):
    for name, func in HAND_RANKINGS:
        result, ranks = func(hand)
        if result:
            return name, ranks
    return "Unknown", []

def get_best_hand(cards):
    best = None
    best_rank = 10
    best_ranks = []
    for combo in itertools.combinations(cards, 5):
        htype, ranks = classify_hand(combo)
        rank_idx = [name for name, _ in HAND_RANKINGS].index(htype)
        if rank_idx < best_rank:
            best = combo
            best_rank = rank_idx
            best_ranks = ranks
        elif rank_idx == best_rank:
            for r1, r2 in zip(ranks, best_ranks):
                if RANK_VALUES[r1] > RANK_VALUES[r2]:
                    best = combo
                    best_ranks = ranks
                    break
                elif RANK_VALUES[r1] < RANK_VALUES[r2]:
                    break
    return list(best)

def compare_hands(h1, h2):
    best1 = get_best_hand(h1)
    best2 = get_best_hand(h2)
    t1, r1 = classify_hand(best1)
    t2, r2 = classify_hand(best2)
    idx1 = [name for name, _ in HAND_RANKINGS].index(t1)
    idx2 = [name for name, _ in HAND_RANKINGS].index(t2)

    if idx1 < idx2:
        return 'player1'
    elif idx1 > idx2:
        return 'player2'
    for a, b in zip(r1, r2):
        if RANK_VALUES[a] > RANK_VALUES[b]:
            return 'player1'
        elif RANK_VALUES[a] < RANK_VALUES[b]:
            return 'player2'
    return 'chop'

def get_best_hand_stage(hand, board):
    return get_best_hand(hand + board)


def compare_cards(card1, card2):
    if RANK_VALUES[card1.rank] > RANK_VALUES[card2.rank]:
        return 1
    elif RANK_VALUES[card1.rank] < RANK_VALUES[card2.rank]:
        return -1
    else:
        # Tiebreaker by suit if ranks equal
        suit_order = {'♠': 4, '♥': 3, '♦': 2, '♣': 1}
        return suit_order[card1.suit] - suit_order[card2.suit]
