from deck import Deck
from holdem import get_best_hand_stage, classify_hand, compare_hands


def start_game(dealer, beginner):
    print("\n=== Starting New Hand ===")
    deck = Deck()
    pot = 0
    board, pot, status = play_round(dealer, beginner, deck, pot)

    if status == 'ended':
        return  # hand ended from fold

    # Final showdown
    print("\n=== SHOWDOWN ===")
    hand1 = dealer.hand + board
    hand2 = beginner.hand + board

    winner = compare_hands(hand1, hand2)
    if winner == 'player1':
        print(f"{dealer.name} wins the pot of {pot} chips!")
        dealer.chips += pot
    elif winner == 'player2':
        print(f"{beginner.name} wins the pot of {pot} chips!")
        beginner.chips += pot
    else:
        print("It's a chop!")
        dealer.chips += pot // 2
        beginner.chips += pot - pot // 2

def betting_stage(first, second, pot, current_bet=0):
    """
    first: Player who acts first in the round
    second: Player who acts second
    pot: current pot
    current_bet: amount already on the table
    """
    print(f"\n=== Betting Round ===")

    # First player action
    print(f"\n{first.name}'s turn:")
    print("1. Check" if current_bet == 0 else f"1. Call ({current_bet} chip)")
    print("2. Raise")
    print("3. All-in")
    print("4. Fold")

    choice1 = input("Choose your action: ")
    if choice1 == '1':
        if current_bet > 0:
            _, pot = first.call(to_call=current_bet, pot=pot)
        else:
            print(f"{first.name} checks.")
    elif choice1 == '2':
        amount, pot = first.raise_bet(current_bet=current_bet, pot=pot)
        current_bet = amount
    elif choice1 == '3':
        amount, pot = first.all_in(pot=pot)
        current_bet = amount
    elif choice1 == '4':
        print(f"{first.name} folds. {second.name} wins the pot of {pot} chips!")
        second.chips += pot
        return pot, 'ended'
    else:
        print("Invalid input. Defaulting to check/call.")
        if current_bet > 0:
            _, pot = first.call(to_call=current_bet, pot=pot)

    # Second player action
    print(f"\n{second.name}'s turn:")
    print("1. Check" if current_bet == 0 else f"1. Call ({current_bet} chip)")
    print("2. Raise")
    print("3. All-in")
    print("4. Fold")

    choice2 = input("Choose your action: ")
    if choice2 == '1':
        if current_bet > 0:
            _, pot = second.call(to_call=current_bet, pot=pot)
        else:
            print(f"{second.name} checks.")
    elif choice2 == '2':
        amount, pot = second.raise_bet(current_bet=current_bet, pot=pot)
        current_bet = amount
        # back to first player to respond
        print(f"\n{first.name}'s turn to respond to raise:")
        print(f"1. Call ({current_bet} chip)")
        print("2. All-in")
        print("3. Fold")
        resp = input("Choose your action: ")
        if resp == '1':
            _, pot = first.call(to_call=current_bet, pot=pot)
        elif resp == '2':
            _, pot = first.all_in(pot=pot)
        elif resp == '3':
            print(f"{first.name} folds. {second.name} wins the pot of {pot} chips!")
            second.chips += pot
            return pot, 'ended'
    elif choice2 == '3':
        amount, pot = second.all_in(pot=pot)
        current_bet = amount
        # first player responds
        print(f"\n{first.name}'s turn to respond to all-in:")
        print(f"1. Call ({current_bet} chip)")
        print("2. Fold")
        resp = input("Choose your action: ")
        if resp == '1':
            _, pot = first.call(to_call=current_bet, pot=pot)
        else:
            print(f"{first.name} folds. {second.name} wins the pot of {pot} chips!")
            second.chips += pot
            return pot, 'ended'
    elif choice2 == '4':
        print(f"{second.name} folds. {first.name} wins the pot of {pot} chips!")
        first.chips += pot
        return pot, 'ended'
    else:
        print("Invalid input. Defaulting to check/call.")
        if current_bet > 0:
            _, pot = second.call(to_call=current_bet, pot=pot)

    return pot, 'continue'

def play_round(dealer, beginner, deck, pot):
    board = []
    def deal_stage(stage_name, num_cards):
        deck.deal(1)  # Burn
        new_cards = deck.deal(num_cards)
        board.extend(new_cards)
        print(f"\n=== {stage_name.upper()} ===")
        print(f"{stage_name.capitalize()} cards:", new_cards if num_cards > 1 else new_cards[0])

        # Show current best hands
        best1 = get_best_hand_stage(dealer.hand, board)
        best2 = get_best_hand_stage(beginner.hand, board)
        print(f"{dealer.name}'s best hand: {best1} ({classify_hand(best1)[0]})")
        print(f"{beginner.name}'s best hand: {best2} ({classify_hand(best2)[0]})")

        return best1, best2
    # === FLOP ===
    deal_stage("flop", 3)
    pot, status = betting_stage(beginner, dealer, pot)
    if status == 'ended':
        return board, pot, 'ended'
    elif status == 'allin':
        # skip turn & river bets
        deck.deal(1)  # burn before turn
        board.extend(deck.deal(1))
        deck.deal(1)  # burn before river
        board.extend(deck.deal(1))
        return board, pot, 'allin'

    # === TURN ===
    deal_stage("turn", 1)
    pot, status = betting_stage(beginner, dealer, pot)
    if status == 'ended':
        return board, pot, 'ended'
    elif status == 'allin':
        # skip river bet
        deck.deal(1)  # burn
        board.extend(deck.deal(1))
        return board, pot, 'allin'

    # === RIVER ===
    deal_stage("river", 1)
    pot, status = betting_stage(beginner, dealer, pot)
    return board, pot, status
