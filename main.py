# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from player import Player
from deck import Deck, compare_cards
from engine import start_game
from holdem import get_best_hand_stage, classify_hand, compare_hands,compare_hands
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♣', '♦']
RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
               '7': 7, '8': 8, '9': 9, 'T': 10,
               'J': 11, 'Q': 12, 'K': 13, 'A': 14}
SUIT_VALUES = {'♠': 4, '♥': 3, '♦': 2, '♣': 1}

def main():
    print("Welcome to Heads-Up Texas Hold’em!")
    name = input("Enter your name: ")
    chip_input = input("Enter starting chips (default 100): ")
    try:
        chips = int(chip_input)
    except:
        chips = 100

    player = Player(name, chips = chips)
    bot = Player("GOD HAND", chips= 100, is_bot=True)

    # First hand: draw for roles
    deck = Deck()
    print("\nDrawing one card each to decide first dealer...")
    card1 = deck.deal(1)[0]
    card2 = deck.deal(1)[0]
    print(f"{player.name} draws: {card1}")
    print(f"{bot.name} draws: {card2}")

    if compare_cards(card1, card2) > 0:
        dealer, beginner = player, bot
    else:
        dealer, beginner = bot, player

    print(f"\nFirst dealer: {dealer.name}")
    print(f"First beginner: {beginner.name}")

    hand_count = 0

    while True:
        # End game if someone is out of chips
        if player.chips <= 0 or bot.chips <= 0:
            break

        print("\n--- Game Menu ---")
        print("1. Start Next Hand")
        print("2. End Game")
        choice = input("Enter your choice: ")

        if choice == '2':
            break
        elif choice != '1':
            print("Invalid input. Try again.")
            continue

        hand_count += 1
        print(f"\n=== HAND {hand_count} START ===")
        start_game(dealer, beginner)

        print(f"\nCurrent chips:")
        print(f"{player.name}: {player.chips}")
        print(f"{bot.name}: {bot.chips}")

        # Swap roles
        dealer, beginner = beginner, dealer

    # Game over summary
    print("\n=== GAME OVER ===")
    print(f"Total hands played: {hand_count}")
    if player.chips == 0:
        print(f"{player.name} is out of chips. {bot.name} wins!")
    elif bot.chips == 0:
        print(f"{bot.name} is out of chips. {player.name} wins!")
    else:
        print("Game ended by user.")

    print(f"\nFinal chip counts:")
    print(f"{player.name}: {player.chips}")
    print(f"{bot.name}: {bot.chips}")

def print_menu_block(title: str, lines: list[str], pad_char: str = '-'):
    max_len = max(len(title.strip()) + 4, max(len(line) for line in lines))
    centered_title = f" {title.strip()} ".center(max_len, pad_char)
    print("\n" + centered_title)

    for line in lines:
        print(line.ljust(max_len))

    print(pad_char * max_len)
    return max_len  # optional

def print_centered_title(title, content_lines, pad_char='-'):
    max_len = max(len(title) + 4, max(len(line) for line in content_lines))
    centered_title = f" {title} ".center(max_len, pad_char)
    print(centered_title)
    return max_len
def print_main_menu():
    options = [
        "1. Start Game",
        "2. Help",
        "3. Quit"
    ]
    print_menu_block("Texas Hold'em Trainer", options)
def show_help_menu():
    while True:
        menu_options = [
            "1. Game Rules",
            "2. Poker Hand Rankings",
            "3. Exit Help"
        ]
        print_menu_block("Help Menu", menu_options)

        choice = input("Please select an option (1-3): ")

        if choice == '1':
            rules = [
                "This is a simplified 1v1 Texas Hold'em trainer.",
                "Each player is dealt 2 hole cards.",
                "Five community cards are revealed (Flop, Turn, River).",
                "Dealer is always the last player to decide in this game.",
                "The goal is to make the best 5-card hand."
            ]
            print_menu_block("Game Rules", rules)

        elif choice == '2':
            hands = [
                "1. Straight Flush – Five cards in a row, same suit (e.g., 5♠ 6♠ 7♠ 8♠ 9♠)",
                "2. Four of a Kind – Four cards of the same rank (e.g., K♠ K♥ K♦ K♣ 3♦)",
                "3. Full House – Three of a kind + a pair (e.g., 9♠ 9♥ 9♦ J♣ J♦)",
                "4. Flush – Five cards of the same suit (e.g., 2♣ 5♣ 8♣ Q♣ K♣)",
                "5. Straight – Five cards in sequence, any suits (e.g., 4♦ 5♣ 6♠ 7♠ 8♥)",
                "6. Three of a Kind – Three cards of same rank (e.g., A♣ A♦ A♠ 6♣ 2♥)",
                "7. Two Pair – Two different pairs (e.g., Q♠ Q♣ 8♦ 8♥ 5♣)",
                "8. One Pair – One pair (e.g., J♦ J♠ 3♣ 7♥ 9♠)",
                "9. High Card – No matching cards (e.g., A♠ 7♦ 6♣ 3♥ 2♠)"
            ]
            print_menu_block("Hand Rankings", hands)

        elif choice == '3':
            print("Exiting help menu.\n")
            break

        else:
            print("Invalid option. Please enter 1, 2, or 3.\n")

# the stage of pre-flop
def pre_flop(dealer, beginner, deck, pot):
    # Deal hole cards
    beginner.hand += deck.deal()
    dealer.hand += deck.deal()
    beginner.hand += deck.deal()
    dealer.hand += deck.deal()
    print(f"{dealer.name}'s hand: {dealer.hand}")
    print(f"{beginner.name}'s hand: {beginner.hand}")

    # Post blind
    blind_amount = 1
    print(f"{beginner.name} posts blind of {blind_amount} chip.")
    beginner.chips -= blind_amount
    pot += blind_amount
    current_bet = blind_amount

    # Dealer acts first
    print(f"\n{dealer.name}'s turn:")
    print("1. Fold")
    print(f"2. Call ({blind_amount} chip)")
    print("3. Raise")
    print("4. All-in")
    choice = input("Choose your action: ")

    if choice == '1':
        print(f"{dealer.name} folds. {beginner.name} wins the pot of {pot} chips!")
        beginner.chips += pot
        return False  # hand ends
    elif choice == '2':
        _, pot = dealer.call(to_call=blind_amount, pot=pot)
        return True  # proceed to flop
    elif choice == '3':
        amount, pot = dealer.raise_bet(current_bet=blind_amount, pot=pot)
        current_bet = amount
    elif choice == '4':
        amount, pot = dealer.all_in(pot=pot)
        current_bet = amount
    else:
        print("Invalid input. Defaulting to call.")
        _, pot = dealer.call(to_call=blind_amount, pot=pot)
        return True

    # Beginner must respond to raise/all-in
    to_call = current_bet - blind_amount
    print(f"\n{beginner.name}'s turn to respond:")
    print(f"1. Fold")
    print(f"2. Call ({to_call} chip)")
    print("3. All-in")
    response = input("Choose your action: ")

    if response == '1':
        print(f"{beginner.name} folds. {dealer.name} wins the pot of {pot} chips!")
        dealer.chips += pot
        return False
    elif response == '2':
        _, pot = beginner.call(to_call=to_call, pot=pot)
        return True
    elif response == '3':
        _, pot = beginner.all_in(pot=pot)
        return True
    else:
        print("Invalid input. Defaulting to fold.")
        dealer.chips += pot
        return False



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
