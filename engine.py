from deck import Deck
from holdem import get_best_hand_stage, classify_hand, compare_hands
# print the chips summary for both player
def print_chip_summary(dealer, beginner):
    print(f"\n--- Chip Count ---")
    print(f"{dealer.name}: {dealer.chips} chips")
    print(f"{beginner.name}: {beginner.chips} chips")
    print("-------------------\n")
from deck import Deck
from holdem import compare_hands
from holdem import get_best_hand_stage, classify_hand

def start_game(dealer, beginner):
    print("\n=== NEW HAND ===")
    deck = Deck()
    pot = 0

    # Pre-flop handles hole cards, blind, and dealer action
    pot, status = pre_flop(dealer, beginner, deck, pot)
    if status == 'ended':
        return  # someone folded

    board = []

    if status == 'allin':
        # All-in happened pre-flop — reveal board with burn cards
        deck.deal(1)  # burn
        board += deck.deal(3)  # flop
        deck.deal(1)  # burn
        board += deck.deal(1)  # turn
        deck.deal(1)  # burn
        board += deck.deal(1)  # river

        print(f"\nBoard: {board}")

        for player in (dealer, beginner):
            best = get_best_hand_stage(player.hand, board)
            hand_type = classify_hand(best)[0]
            print(f"{player.name}'s best hand: {best} ({hand_type})")

    else:
        # Play normally
        board, pot, status = play_round(dealer, beginner, deck, pot)
        if status == 'ended':
            return

    # === SHOWDOWN ===
    print("\n=== SHOWDOWN ===")
    print(f"Board: {board}")
    print(f"Pot: {pot}")

    full1 = dealer.hand + board
    full2 = beginner.hand + board
    result = compare_hands(full1, full2)

    if result == 'player1':
        print(f"{dealer.name} wins the pot of {pot} chips!")
        dealer.chips += pot
    elif result == 'player2':
        print(f"{beginner.name} wins the pot of {pot} chips!")
        beginner.chips += pot
    else:
        print("Chop! Pot split.")
        dealer.chips += pot // 2
        beginner.chips += pot - pot // 2

def pre_flop(dealer, beginner, deck, pot):
    # Deal hole cards in proper order
    beginner.hand = [deck.deal(1)[0]]
    dealer.hand = [deck.deal(1)[0]]
    beginner.hand.append(deck.deal(1)[0])
    dealer.hand.append(deck.deal(1)[0])

    print(f"{beginner.name}'s hand: {beginner.hand}")
    print(f"{dealer.name}'s hand: {dealer.hand}")

    # Post blind
    blind = 1
    print(f"{beginner.name} posts blind of {blind} chip.")
    beginner.chips -= blind
    pot += blind
    current_bet = blind

    # Dealer acts
    print(f"\n{dealer.name}'s turn:")
    print("1. Fold")
    print(f"2. Call ({blind})")
    print("3. Raise")
    print("4. All-in")
    action = input("Choose action: ")

    if action == '1':
        print(f"{dealer.name} folds. {beginner.name} wins the pot of {pot} chips.")
        beginner.chips += pot
        return pot, 'ended'
    elif action == '2':
        _, pot = dealer.call(to_call=blind, pot=pot)
        return pot, 'continue'
    elif action == '3':
        amount, pot = dealer.raise_bet(current_bet=blind, pot=pot)
        current_bet = amount
    elif action == '4':
        amount, pot = dealer.all_in(pot=pot)
        current_bet = amount
    else:
        print("Invalid input. Defaulting to call.")
        _, pot = dealer.call(to_call=blind, pot=pot)
        return pot, 'continue'

    # Beginner must respond
    print(f"\n{beginner.name}'s turn to respond:")
    print(f"1. Fold")
    print(f"2. Call ({current_bet - blind})")
    print("3. All-in")
    response = input("Choose action: ")

    if response == '1':
        print(f"{beginner.name} folds. {dealer.name} wins the pot of {pot} chips.")
        dealer.chips += pot
        return pot, 'ended'
    elif response == '2':
        _, pot = beginner.call(to_call=current_bet - blind, pot=pot)
        return pot, 'continue'
    elif response == '3':
        _, pot = beginner.all_in(pot=pot)
        return pot, 'allin'
    else:
        print("Invalid input. Defaulting to fold.")
        dealer.chips += pot
        return pot, 'ended'
def betting_stage(first, second, pot, current_bet=0):
    print(f"\n=== Betting Round ===")

    # First player acts
    print(f"\n{first.name}'s turn:")
    print("1. Check" if current_bet == 0 else f"1. Call ({current_bet})")
    print("2. Raise")
    print("3. All-in")
    print("4. Fold")
    choice1 = input("Choose your action: ")

    if choice1 == '1':
        if current_bet > 0:
            _, pot = first.call(current_bet, pot)
    elif choice1 == '2':
        amount, pot = first.raise_bet(current_bet, pot)
        current_bet = amount
    elif choice1 == '3':
        amount, pot = first.all_in(pot)
        current_bet = amount

        # Second player responds once to all-in
        print(f"\n{second.name}'s turn to respond to all-in:")
        print(f"1. Call ({current_bet})")
        print("2. All-in")
        print("3. Fold")
        resp = input("Choose: ")

        if resp == '1':
            _, pot = second.call(to_call=current_bet, pot=pot)
            return pot, 'allin'
        elif resp == '2':
            _, pot = second.all_in(pot)
            return pot, 'allin'
        else:
            print(f"{second.name} folds. {first.name} wins {pot} chips!")
            first.chips += pot
            return pot, 'ended'
    elif choice1 == '4':
        print(f"{first.name} folds. {second.name} wins {pot} chips!")
        second.chips += pot
        return pot, 'ended'
    else:
        if current_bet > 0:
            _, pot = first.call(current_bet, pot)

    # Second player acts (only if no all-in from first)
    print(f"\n{second.name}'s turn:")
    print("1. Check" if current_bet == 0 else f"1. Call ({current_bet})")
    print("2. Raise")
    print("3. All-in")
    print("4. Fold")
    choice2 = input("Choose your action: ")

    if choice2 == '1':
        if current_bet > 0:
            _, pot = second.call(current_bet, pot)
    elif choice2 == '2':
        amount, pot = second.raise_bet(current_bet, pot)
        current_bet = amount
        # First player responds to raise
        print(f"\n{first.name}'s turn to respond:")
        print(f"1. Call ({current_bet})")
        print("2. All-in")
        print("3. Fold")
        resp = input("Choose: ")
        if resp == '1':
            _, pot = first.call(current_bet, pot)
        elif resp == '2':
            _, pot = first.all_in(pot)
            return pot, 'allin'
        else:
            print(f"{first.name} folds. {second.name} wins {pot} chips!")
            second.chips += pot
            return pot, 'ended'
    elif choice2 == '3':
        amount, pot = second.all_in(pot)
        current_bet = amount
        print(f"\n{first.name}'s turn to respond to all-in:")
        print(f"1. Call ({current_bet})")
        print("2. Fold")
        resp = input("Choose: ")
        if resp == '1':
            _, pot = first.call(current_bet, pot)
            return pot, 'allin'
        else:
            print(f"{first.name} folds. {second.name} wins {pot} chips!")
            second.chips += pot
            return pot, 'ended'
    elif choice2 == '4':
        print(f"{second.name} folds. {first.name} wins {pot} chips!")
        first.chips += pot
        return pot, 'ended'
    else:
        if current_bet > 0:
            _, pot = second.call(current_bet, pot)

    return pot, 'continue'





def play_round(dealer, beginner, deck, pot):
    board = []

    def deal_stage(name, count):
        deck.deal(1)  # burn
        cards = deck.deal(count)
        board.extend(cards)
        print(f"\n=== {name.upper()} ===")
        print(f"Board: {board}")

        for player in (dealer, beginner):
            best = get_best_hand_stage(player.hand, board)
            hand_type = classify_hand(best)[0]
            print(f"{player.name}'s best hand: {best} ({hand_type})")

        return cards

    # FLOP
    deal_stage("flop", 3)
    pot, status = betting_stage(beginner, dealer, pot)
    print(f"Current pot: {pot}")
    if status in ("ended", "allin"):
        if status == "allin":
            deal_stage("turn", 1)
            deal_stage("river", 1)
        return board, pot, status

    # TURN
    deal_stage("turn", 1)
    pot, status = betting_stage(beginner, dealer, pot)
    print(f"Current pot: {pot}")
    if status in ("ended", "allin"):
        if status == "allin":
            deal_stage("river", 1)
        return board, pot, status

    # RIVER
    deal_stage("river", 1)
    pot, status = betting_stage(beginner, dealer, pot)
    print(f"Current pot: {pot}")
    return board, pot, status
