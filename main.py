# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import deck,player


def main():
    # ask player's name
    name = input('please enter your name')
    # enter player's chip
    chip = input('please enter how many chips you wanna start (default is 100)')
    # tips
    print('Before the game start, this game is designed to train player 1v1 skill in Texas Hodem poker, and the blind 1')
    p = player.Player(name,chip)
    # draw a card to start who will be the first dealer
    while True:



# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
