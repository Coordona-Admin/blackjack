import os
import random


def create_deck():

    # create a deck of cards
    deck = []
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['♣️', '♦️', '♥️', '♠️']
    for suit in suits:
        for value in values:
            card = f"{value}{suit}"
            deck.append(card)
            
    return deck

def create_shoe(number_of_decks:int):
    shoe = []
    for i in range(number_of_decks):
        shoe.extend(create_deck())
    return shoe

def shuffle_shoe(shoe:list):
    random.shuffle(shoe)
    return shoe

def deal_card(shoe:list, number_of_cards:int):
    cards = []
    for i in range(number_of_cards):
        cards.append(shoe.pop())
    return cards

def print_hand(hand:list, mask_first_card:bool=False, show_score:bool=False):
    for card_number, card in enumerate(hand):
        if mask_first_card and card_number == 0:
            print(f"XX ", end="")
        else:
            print(f"{card} ", end="")

    if show_score:
        print("  Score: ", score_hand(hand))
    print()

def show_table(dealer_hand:list, player_hand:list, mask_dealer:bool=True, 
               show_player_score:bool=False, show_dealer_score:bool=False):
    
    os.system("cls")
    print("Dealer's Hand")  
    print_hand(dealer_hand, show_score=show_dealer_score, mask_first_card=mask_dealer)
    print("Player's Hand")
    print_hand(player_hand, show_score=show_player_score)

def score_hand(hand:list) -> int:
    score = 0
    for card in hand:
        if "2" in card:
            score += 2
        if "3" in card:
            score += 3
        if "4" in card:
            score += 4
        if "5" in card:
            score += 5
        if "6" in card:
            score += 6
        if "7" in card:
            score += 7
        if "8" in card:
            score += 8
        if "9" in card:
            score += 9
        if "10" in card:
            score += 10
        if "J" in card:
            score += 10
        if "Q" in card:
            score += 10
        if "K" in card:
            score += 10
        if "A" in card and score > 10:
            score += 1
        if "A" in card and score <= 10:
            score += 11
    return score

def print_results(player_hand:list, dealer_hand:list) -> None:
    if score_hand(player_hand) > 21:
        print("You busted - You lose!")
    elif score_hand(dealer_hand) > 21:
        print("Delaer busted - You Won!")
    elif score_hand(player_hand) > score_hand(dealer_hand):
        print("You Win!")
    elif score_hand(player_hand) < score_hand(dealer_hand):
        print("You Lose!")
    elif score_hand(player_hand) == score_hand(dealer_hand):
        print("It's a Push!")

def play_blackjack():
    os.system("cls")
    
    player_busted = False
    
    shoe = create_shoe(5)
    shoe = shuffle_shoe(shoe)

    # Deal the initial hands
    dealer_hand = deal_card(shoe, 2)
    player_hand = deal_card(shoe, 2)

    show_table(dealer_hand, player_hand, mask_dealer=True, show_player_score=True)

    # If the player has a blackjack then we're done
    if score_hand(player_hand) != 21:

        # Loop until player stands or busts
        while True:
            user_input = input("(H)it or (S)tand? ").lower()
            if user_input == "h":
                player_hand.extend(deal_card(shoe, 1))
                show_table(dealer_hand, player_hand, mask_dealer=True, show_player_score=True)

            if user_input == "s":
                break

            if user_input not in ["h","s"]:
                print("Please enter either 'H' or'S'.   Try harder.")

            if score_hand(player_hand) > 21:
                player_busted = True
                break

        while (17 > score_hand(dealer_hand) <= 21) and (not player_busted):
            dealer_hand.extend(deal_card(shoe, 1))

    show_table(dealer_hand, player_hand, mask_dealer=False, show_player_score=True, show_dealer_score=True)
    print_results(player_hand, dealer_hand)
    
if __name__ == '__main__':
    while True:
        play_blackjack()

        play_again_input = input("Would you like to play again? (Y/N) ").lower()
        if play_again_input != "y":
            break
        