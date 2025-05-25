from deck import Deck
from bot import bot_decide
from holdem import classify_hand, get_best_hand_stage, compare_hands
from player import Player

def parse_action_input(player_name, options, chips=None):
    print(f"\n{player_name}'s turn:")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt.capitalize()}")
    choice = input("Choose an option: ")
    action_map = {str(i): opt for i, opt in enumerate(options, 1)}
    action = action_map.get(choice, 'fold')

    if action == 'raise' and chips is not None:
        while True:
            try:
                amount = int(input(f"How many chips do you want to raise? (You have {chips}): "))
                if 1 <= amount <= chips:
                    return ('raise', amount)
                else:
                    print("Invalid amount. Must be between 1 and your total chips.")
            except ValueError:
                print("Please enter a valid number.")

    return action

def start_game(player1, player2):
    print("\n=== NEW HAND ===")
    deck = Deck()
    pot = 0

    player1.hand = deck.deal(2)
    player2.hand = deck.deal(2)

    print(f"{player1.name}'s hand: {player1.hand}")
    if not player2.is_bot:
        print(f"{player2.name}'s hand: {player2.hand}")

    pot, side_pot, status, contributions = betting_stage(player1, player2, pot)
    if status == 'ended':
        return

    board = []
    if status == 'allin':
        deck.deal(1)
        board += deck.deal(3)
        deck.deal(1)
        board += deck.deal(1)
        deck.deal(1)
        board += deck.deal(1)
    else:
        deck.deal(1)
        board += deck.deal(3)
        print(f"\n=== FLOP ===\nBoard: {board}")
        pot, side_pot, status, contributions = betting_stage(player1, player2, pot, current_bet=0)
        if status == 'ended':
            return

        if status != 'allin':
            deck.deal(1)
            board += deck.deal(1)
            print(f"\n=== TURN ===\nBoard: {board}")
            pot, side_pot, status, contributions = betting_stage(player1, player2, pot, current_bet=0)
            if status == 'ended':
                return

            if status != 'allin':
                deck.deal(1)
                board += deck.deal(1)
                print(f"\n=== RIVER ===\nBoard: {board}")
                pot, side_pot, status, contributions = betting_stage(player1, player2, pot, current_bet=0)
                if status == 'ended':
                    return

    print("\n=== SHOWDOWN ===")
    print(f"Board: {board}")
    print(f"{player1.name}'s hand: {player1.hand}")
    print(f"{player2.name}'s hand: {player2.hand}")

    best1 = get_best_hand_stage(player1.hand, board)
    best2 = get_best_hand_stage(player2.hand, board)
    t1, _ = classify_hand(best1)
    t2, _ = classify_hand(best2)
    print(f"\n{player1.name}'s best hand: {best1} ({t1})")
    print(f"{player2.name}'s best hand: {best2} ({t2})")

    c1 = contributions[player1.name]
    c2 = contributions[player2.name]
    main_pot = min(c1, c2) * 2
    side_pot = abs(c1 - c2)

    print(f"\nMain Pot: {main_pot}, Side Pot: {side_pot}")
    result = compare_hands(player1.hand + board, player2.hand + board)

    if result == 'player1':
        print(f"\n{player1.name} wins the main pot of {main_pot} chips!")
        player1.chips += main_pot
        if c1 > c2:
            print(f"{player1.name} also wins the side pot of {side_pot} chips.")
            player1.chips += side_pot
    elif result == 'player2':
        print(f"\n{player2.name} wins the main pot of {main_pot} chips!")
        player2.chips += main_pot
        if c2 > c1:
            print(f"{player2.name} also wins the side pot of {side_pot} chips.")
            player2.chips += side_pot
    else:
        print("\nChop! Main pot is split.")
        player1.chips += main_pot // 2
        player2.chips += main_pot - (main_pot // 2)

def betting_stage(p1, p2, pot, current_bet=1):
    side_pot = 0
    actions = {}
    players = [p1, p2]
    idx = 0
    contributions = {p1.name: 0, p2.name: 0}
    while True:
        player = players[idx]
        opponent = players[1 - idx]
        to_call = current_bet - contributions[player.name]
        print(f"\n{player.name}'s turn:")
        print(f"Chips: {player.chips}, To call: {to_call}, Pot: {pot}")

        if player.is_bot:
            decision = bot_decide('flop', player.hand, [], to_call, pot, is_blind=(player == p2), bot_chips=player.chips)

            if isinstance(decision, tuple) and decision[0] == 'raise':
                action, raise_pct = decision
                raise_amount = int(min(player.chips, max(to_call + 1, int(pot * raise_pct))))
            else:
                action = decision
                raise_amount = None
        else:
            options = ['fold', 'call', 'raise', 'all-in'] if player.chips > 0 else ['fold']
            result = parse_action_input(player.name, options, chips=player.chips)
            if isinstance(result, tuple):
                action, raise_amount = result
            else:
                action = result
                raise_amount = None

        if action == 'fold':
            return opponent.fold(player, pot) + ('ended', contributions)

        elif action == 'call':
            amount, pot = player.call(to_call, pot)
            contributions[player.name] += amount
            actions[player.name] = 'call'

        elif action == 'raise':
            if raise_amount >= player.chips:
                amount, pot = player.all_in(pot)
                contributions[player.name] += amount
                return pot, 0, 'allin', contributions
            else:
                amount, pot = player.bet_or_raise(current_bet, pot, amount=raise_amount)
                current_bet = contributions[player.name] + amount
                contributions[player.name] += amount
                actions = {}
                actions[player.name] = 'raise'

        elif action == 'all-in':
            all_in_amount = player.chips
            print(f"{player.name} goes all-in with {all_in_amount}!")
            player.chips = 0
            pot += all_in_amount
            contributions[player.name] += all_in_amount
            current_bet = contributions[player.name]  # now reflects full all-in

            if opponent.chips == 0:
                return pot, 0, 'allin', contributions

            print(f"\n{opponent.name}'s turn to respond to all-in:")
            to_call = current_bet - contributions[opponent.name]
            print(f"Chips: {opponent.chips}, To call: {to_call}")

            if opponent.is_bot:
                decision = bot_decide('flop', player.hand, [], to_call, pot, is_blind=(player == p2), bot_chips=player.chips)

                if decision == 'fold':
                    return opponent.fold(player, pot) + ('ended', contributions)
                else:
                    call_amount = min(to_call, opponent.chips)
                    amount, pot = opponent.call(call_amount, pot)
                    contributions[opponent.name] += amount
                    side_pot = max(0, to_call - call_amount)
                    return pot, side_pot, 'allin', contributions
            else:
                options = ['fold', 'call']
                result = parse_action_input(opponent.name, options, chips=opponent.chips)
                if result == 'fold':
                    return opponent.fold(player, pot) + ('ended', contributions)
                else:
                    call_amount = min(to_call, opponent.chips)
                    amount, pot = opponent.call(call_amount, pot)
                    contributions[opponent.name] += amount
                    side_pot = max(0, to_call - call_amount)
                    return pot, side_pot, 'allin', contributions

        idx = 1 - idx
        if p1.chips == 0 or p2.chips == 0:
            return pot, 0, 'allin', contributions
        if actions.get(p1.name) == 'call' and actions.get(p2.name) == 'call':
            break

    return pot, 0, 'continue', contributions
