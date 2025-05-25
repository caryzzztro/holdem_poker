
import random
from holdem import classify_hand, get_best_hand_stage, RANK_VALUES

STRONG_RANKS = ['A', 'K', 'Q', 'J', 'T']
PAIR_VALUES = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7']

def bot_has_nuts(hand, board):
    full_hand = hand + board
    best5 = get_best_hand_stage(hand, board)
    hand_type, rank_list = classify_hand(best5)

    if hand_type in ['Straight Flush', 'Four of a Kind']:
        return True

    if hand_type == 'Full House':
        ranks = [card.rank for card in full_hand]
        common_rank = max(set(ranks), key=ranks.count)
        board_ranks = [card.rank for card in board]
        if ranks.count(common_rank) >= 3 and common_rank not in board_ranks:
            return True

    if hand_type == 'Three of a Kind':
        suits = [card.suit for card in board]
        flush_possible = any(suits.count(s) >= 2 for s in suits)
        if not flush_possible:
            return True

    return False

def estimate_ev(to_call, pot, win_chance):
    call_ev = win_chance * pot - (1 - win_chance) * to_call
    raise_ev = win_chance * (pot + to_call) - (1 - win_chance) * (2 * to_call)
    return call_ev, raise_ev

def bot_decide(stage, bot_hand, board, to_call, pot, is_blind, bot_chips):
    full_hand = bot_hand + board
    if len(bot_hand + board) < 5:
        ranks = sorted([card.rank for card in bot_hand], key=lambda r: RANK_VALUES[r], reverse=True)
        suited = bot_hand[0].suit == bot_hand[1].suit
        is_pair = bot_hand[0].rank == bot_hand[1].rank

        if is_pair and RANK_VALUES[bot_hand[0].rank] >= 10:
            return ('raise', 0.5)
        elif is_pair or suited or RANK_VALUES[ranks[0]] >= 11:
            return 'call'
        else:
            return 'fold'
    else:
        best5 = get_best_hand_stage(bot_hand, board)
        hand_type, rank_list = classify_hand(best5)

    hand_strengths = {
        'High Card': 0.2,
        'Pair': 0.4,
        'Two Pair': 0.55,
        'Three of a Kind': 0.65,
        'Straight': 0.75,
        'Flush': 0.8,
        'Full House': 0.9,
        'Four of a Kind': 0.95,
        'Straight Flush': 0.99
    }
    win_chance = hand_strengths.get(hand_type, 0.3)

    if bot_has_nuts(bot_hand, board):
        return 'all-in' if random.random() < 0.3 else ('raise', random.choice([0.5, 0.7, 1.0]))

    if to_call == 0:
        if win_chance >= 0.7:
            return ('raise', random.choice([0.3, 0.5, 0.7]))
        if hand_type == 'High Card' and random.random() < 0.15:
            return ('raise', random.choice([0.3, 0.5]))
        return 'check'

    # Smart all-in defense: fold to big threats if weak
    risk_ratio = to_call / (bot_chips + 1e-9)
    threshold = 0.65 - (risk_ratio * 0.5)
    if win_chance < threshold:
        return 'fold'

    call_ev, raise_ev = estimate_ev(to_call, pot, win_chance)

    if call_ev < 0 and not is_blind:
        return 'fold'
    elif raise_ev > call_ev and raise_ev > 0:
        return ('raise', random.choice([0.3, 0.5, 0.7, 1.0]))
    elif call_ev >= 0:
        return 'call'
