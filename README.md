# COMP9001 Texas Poker 1v1 Game

This project is a simplified two-player Texas Hold'em Poker game developed in Python for the COMP9001 course. One human player competes against a bot using core poker rules and simplified betting logic, designed for terminal-based gameplay.

## Features

- Standard Texas Hold'em rules: 2 hole cards + 5 community cards
- Betting phases: Pre-flop, Flop, Turn, River
- Bot opponent with risk-aware decision-making logic
- Realistic all-in and side pot handling
- Showdown with hand evaluation and winner declaration
- Option to select bot difficulty via starting chips
- Clear, interactive terminal interface

## How to Run

1. Make sure Python 3 is installed on your system.
2. Download or clone the repository:
   ```
   git clone https://github.com/caryzzztro/holdem_poker.git
   cd comp9001-poker
   ```
3. Run the main script:
   ```
   python main.py
   ```
4. Follow prompts to:
   - Enter your name
   - Choose your chip amount
   - Select bot difficulty (Easy/Medium/Hard/Custom)

## File Structure

- `main.py` – Entry point: sets up the game loop and interface
- `engine.py` – Core logic for betting rounds and game flow
- `bot.py` – Decision engine for the bot’s moves
- `player.py` – Player class with methods like call, raise, fold, all-in
- `deck.py` – Deck and card utilities
- `holdem.py` – Poker hand evaluator and comparator
- `README.md` – Documentation

## Download ZIP

You can download the full project here:

➡️ [Download ZIP](https://github.com/yourusername/comp9001-poker/archive/refs/heads/main.zip)

> (Replace with your actual GitHub repo if applicable.)

## Gameplay Example

```
Welcome to Heads-Up Texas Hold’em!
Enter your name: Ho
Enter starting chips (default 100): 200
Select bot difficulty:
1. Easy (100 chips)
2. Normal (200 chips)
3. Hard (500 chips)
4. Custom
```

## License

This project is licensed for educational and non-commercial use only.

## Author

**Ho Yuen Chan**
**SID: 490537929**
Bachelor of Computer Science  
COMP9001, 2025  
University Submission
