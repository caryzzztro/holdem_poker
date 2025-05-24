# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import deck,player,random
import holdem
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♣', '♦']
RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
               '7': 7, '8': 8, '9': 9, 'T': 10,
               'J': 11, 'Q': 12, 'K': 13, 'A': 14}
SUIT_VALUES = {'♠': 4, '♥': 3, '♦': 2, '♣': 1}


def main():
    # Ask for player's name, can not be same as bot name
    while True:
        name = input("Please enter your name: ")
        if name == 'GOD HAND':
            print("Your name should not be same as bot's name")
        else:
            break

    # Ask for starting chips with default fallback
    chip_input = input("Please enter how many chips you want to start with (default is 100, max is 400): ")
    try:
        if not chip_input.strip():
            chips = 100
        else:
            chips = int(chip_input)
            if chips > 400:
                print("Max starting chips is 400. Setting chips to 400.")
                chips = 400
            elif chips <= 0:
                print("Chip amount must be positive. Using default: 100.")
                chips = 100
    except ValueError:
        print("Invalid input. Using default: 100 chips.")
        chips = 100
    # Game intro tip
    print("\nThis game is designed to train 1v1 Texas Hold'em skills. Blinds are set to 1 chip.")

    # Create player and opponent (not using bot logic yet)  # assuming your Player class is in player.py
    player1 = player.Player(name, chips)
    player2 = player.Player(name="GOD HAND", is_bot=False, chips=100)  # manually controlled for now

    # Draw to decide who deals first (example logic placeholder)

    # Create and shuffle deck
    game_deck = deck.Deck()

    print("\nDrawing one card each to decide dealer...")

    card1 = game_deck.deal(1)[0]
    card2 = game_deck.deal(1)[0]

    print(f"{player1.name} draws: {card1}")
    print(f"{player2.name} draws: {card2}")

    comparison = game_deck.compare_cards(card1, card2)

    if comparison == 1:
        dealer = player1
        beginner = player2
    elif comparison == -1:
        dealer = player2
        beginner = player1
    else:
        dealer = player1  # player1 drew first
        beginner = player2
        print("Cards are tied! First drawer becomes dealer.")

    print(f"\nDealer is: {dealer.name}")
    print(f"Beginner (acts first): {beginner.name}")
    # begin the game
    while True:
        print("Game Start!")
        print_main_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print("Starting game...\n")
            # start_game()
        elif choice == '2':
            show_help_menu()
        elif choice == '3':
            print("Thanks for playing!")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.\n")



def print_centered_title(title, content_lines, pad_char='-'):
    max_len = max(len(title) + 4, max(len(line) for line in content_lines))
    centered_title = f" {title} ".center(max_len, pad_char)
    print(centered_title)
    return max_len
def print_main_menu():
    menu_title = " Texas Hold'em Trainer "
    options = [
        "1. Start Game",
        "2. Help",
        "3. Quit"
    ]

    max_len = max(len(menu_title), max(len(opt) for opt in options)) + 4
    print("\n" + menu_title.center(max_len, "="))

    for opt in options:
        print(opt.center(max_len))

    print("-" * max_len)
def show_help_menu():

    while True:
        menu_options = [
            "1. Game Rules",
            "2. Poker Hand Rankings",
            "3. Exit Help"
        ]

        max_len = max(len(line) for line in menu_options)
        print("\n" + "=== Help Menu ===".center(max_len + 4))
        for option in menu_options:
            print(option.ljust(max_len))
        print("-" * max_len)  # bottom line under the menu

        choice = input("Please select an option (1-3): ")


        if choice == '1':
            rules = [
                "This is a simplified 1v1 Texas Hold'em trainer.",
                "Each player is dealt 2 hole cards.",
                "Five community cards are revealed (Flop, Turn, River).",
                "Dealer is always the last player to decide in thi game",
                "The goal is to make the best 5-card hand."
            ]
            width = print_centered_title("Game Rules", rules)
            for line in rules:
                print(line.ljust(width))
            print("-" * width)

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
            width = print_centered_title("Hand Rankings", hands)
            for line in hands:
                print(line.ljust(width))
            print("-" * width)

        elif choice == '3':
            print("Exiting help menu.\n")
            break

        else:
            print("Invalid option. Please enter 1, 2, or 3.\n")


# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
