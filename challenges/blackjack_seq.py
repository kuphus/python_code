import random
import os

card_types = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
# visibility rules: ALL, FIRST, SECOND, NONE
visibility_rules = "FIRST"
players = []
player_number = None


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def create_deck(number_of_decks, *exclude_cards):
    deck = []
    for i in range(0, number_of_decks):
        for card in card_types:
            if card not in exclude_cards:
                club = "\u2663"+card
                spades = "\u2660"+card
                diamond = "\u2666"+card
                heart = "\u2665"+card
                deck.extend([club, spades, diamond, heart])
    print("The deck has ", str(len(deck)), "cards")
    return deck


def shuffle(deck):
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)


def get_player_info():
    cls()
    amount_players = int(input("How many players? "))
    create_players(amount_players+1)
    your_number = int(input("Which player number are you? "))
    for i in range(1, amount_players+1):
        name = input("What is the name of player " + str(i) + "? ")
        players[i]["name"] = name
    return your_number


def create_players(number_of_players):
    for i in range(0, number_of_players):
        if i == 0:
            temp = {"name": "Dealer",
                    "cards": []
                    }
        else:
            temp = {"name": "",
                    "cards": []
                    }
        players.append(temp)


def deal_cards(players, deck):
    # first card for all players
    for player in players:
        player["cards"].append(deck.pop(0))
    # second card for all players
    for player in players:
        player["cards"].append(deck.pop(0))


def print_field():
    # First build the lines
    offset_left = 15
    player_name_line = " " * offset_left
    player_card_line = " " * offset_left
    for num_p, player in enumerate(players[1:]):
        name_length = len(player["name"])
        whitespace = 40 - name_length
        player_name_line += player["name"] + " " * whitespace
        cards = ""
        for num_c, card in enumerate(player["cards"]):
            if visibility_rules == "FIRST" and num_c == 0 and num_p != player_number:
                cards += "**" + "  "
            elif visibility_rules == "SECOND" and num_c == 1 and num_p != player_number:
                cards += "**" + "  "
            elif visibility_rules == "NONE" and num_p != player_number:
                cards += "**" + "  "
            else:
                cards += card + "  "
        card_length = len(cards)
        whitespace = 40 - card_length
        player_card_line += cards + " " * whitespace
    # For the dealer
    left_offset = int(
        (max(len(player_name_line), len(player_card_line)) - 25) / 2)
    first_line = " " * left_offset + players[0]["name"]
    second_line = " " * left_offset
    for num, card in enumerate(players[0]["cards"]):
        if visibility_rules == "FIRST" and num == 0:
            second_line += "**" + "  "
        elif visibility_rules == "SECOND" and num == 1:
            second_line += "**" + "  "
        elif visibility_rules == "NONE":
            second_line += "**" + "  "
        else:
            second_line += card + "  "
    # Now print the whole field
    cls()
    print("\n\n")
    print(first_line)
    print(second_line)
    print("\n\n\n")
    print(player_name_line)
    print(player_card_line)


def play():
    print("test")


def test():
    for player in players:
        print(player["cards"])


def setup_game():
    deck = create_deck(1)
    print("deck created")
    shuffle(deck)
    print("deck shuffled")
    player_number = get_player_info()
    deal_cards(players, deck)
    print_field()


setup_game()
