import os
import random

from wallet import Wallet


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

def deal_card(shoe:list, number_of_cards:int) -> list:
    cards = []
    for i in range(number_of_cards):
        cards.append(shoe.pop())
    return cards

def print_hand(hand:list, mask_first_card:bool=False, show_score:bool=False) -> None:
    for card_number, card in enumerate(hand):
        if mask_first_card and card_number == 0:
            print(f"XX ", end="")
        else:
            print(f"{card} ", end="")

    if show_score:
        print("  Score: ", score_hand(hand))
    print()

def show_table(dealer_hand:list, player_hand:list, mask_dealer:bool=True, 
               show_player_score:bool=False, show_dealer_score:bool=False) -> None:
    
    os.system("cls")
    print("Dealer's Hand")  
    print_hand(dealer_hand, show_score=show_dealer_score, mask_first_card=mask_dealer)
    print("Player's Hand")
    print_hand(player_hand, show_score=show_player_score)

def score_hand(hand:list) -> int:

    # Move any aces to the end of the list - we need to handle those scores based on the other
    # cards in the hand.  For instance if the player has an A, 3, K unsorted it would bust at 24, but it should be 14.
    sorted_hand = []
    for card in hand:
        if "A" in card:
            # Move the A to the end of the list
            sorted_hand.append(card)
        else:
            # Add the card to the front of the list
            sorted_hand.insert(0, card)
    hand = sorted_hand

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

def game_results(player_hand:list, dealer_hand:list, player_blackjack: bool, bet: int) -> float:

    if player_blackjack:
        print(f"BLACKJACK!  You won{bet * 1.5}")
        return (bet * 1.5)
    
    player_score = score_hand(player_hand)
    dealer_score = score_hand(dealer_hand)
    
    if player_score > 21:
        print(f"You busted - You lose {bet}")
        return -bet
    if dealer_score > 21:
        print(f"Dealer busted - You Won {bet}!")
        return bet
    if player_score > dealer_score:
        print(f"You Win {bet}!")
        return bet
    if player_score < dealer_score:
        print(f"You Lose {bet}!")
        return -bet
    if player_score == dealer_score:
        print("It's a Push!  No money changes hand.")
        return 0
    
    # If we get here we missed something major  :)
    return 0

def print_wallet(wallet:Wallet) -> None:
    print (f"Balance: {wallet.balance}")

def play_blackjack(wallet:Wallet) -> None:
    os.system("cls")
    
    player_busted = False
    player_blackjack = False
    
    shoe = create_shoe(5)
    shoe = shuffle_shoe(shoe)

    # Loop until player gives a valid bet.
    print_wallet(wallet)
    while True:
        bet = input("How much would you like to bet?")
        try:
            bet = float(bet)
            if float(bet) <= 0:
                print("Please enter a positive number.")
                continue
            if float(bet) > wallet.balance:
                print(f"You don't have enough money to bet {bet}.")
                continue
            break

        except ValueError:
            print("Please enter a number.")
            continue

    # Deal the initial hands
    dealer_hand = deal_card(shoe, 2)
    player_hand = deal_card(shoe, 2)

    show_table(dealer_hand, player_hand, mask_dealer=True, show_player_score=True)

    # If the player has a blackjack then we're done
    if score_hand(player_hand) == 21:
        player_blackjack = True
    
    else:
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
    wallet.balance += game_results(player_hand, dealer_hand, player_blackjack, bet)
    
if __name__ == '__main__':

    wallet = Wallet(500)
        
    while True:
        play_blackjack(wallet)

        if wallet.balance <= 0:
            print(f"You lost all your money.  Goodbye!\n\n")
            break

        print_wallet(wallet)
        play_again_input = input("Would you like to play again? (Y/N) ").lower()
        if play_again_input != "y":
            print(f"Thank you for playing!  You ended up with a balance of:{wallet.balance}\n\n")
            break
        