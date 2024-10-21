import random

# Create a shuffled card deck with 4 suites of cards 2-10, and face cards
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
random.shuffle(deck)

# Define a function to get the value of a card in Blackjack
def get_card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11  # In Blackjack, Ace can be 1 or 11, but we'll use 11 as default
    else:
        return card  # For number cards, return their face value

# Create a dictionary to store card values
card_values = {card: get_card_value(card) for card in set(deck)}

# Update the deck to use tuples (card, value)
deck = [(card, card_values[card]) for card in deck]

# Shuffle the deck again after updating
random.shuffle(deck)

#print(deck)


# Function to calculate the total value of a hand
def calculate_hand(hand):
    total = sum(card[1] for card in hand)
    # Adjust for Aces
    num_aces = sum(1 for card in hand if card[0] == 'A')
    while total > 21 and num_aces:
        total -= 10
        num_aces -= 1
    return total

# Function to display a hand
def display_hand(hand, hide_first=False):
    if hide_first:
        return f"[Hidden], {', '.join(str(card[0]) for card in hand[1:])}"
    return ', '.join(str(card[0]) for card in hand)

# Function to get a valid bet
def get_bet(wallet):
    while True:
        bet = input(f"Your wallet: ${wallet}. Enter your bet (or q to quit): $")
        if bet.lower() == 'q':
            return 'q'
        try:
            bet = int(bet)
            if 0 < bet <= wallet:
                return bet
            print("Invalid bet. Please enter an amount within your wallet balance.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

# Initialize wallet
wallet = 1000

# Main game loop
while True:
    print(r'''
        _ _ _ ____ _    ____ ____ _  _ ____    ___ ____
        | | | |___ |    |    |  | |\/| |___     |  |  |
        |_|_| |___ |___ |___ |__| |  | |___     |  |__|
    ''')
    print(r''' 
    
         ,-,---. .              ,-_/                    
          '|___/ |  ,-. ,-. . , '  | ,-. ,-. . ,        
 -- -- -- ,|   \ |  ,-| |   |/     | ,-| |   |/ -- -- --
         `-^---' `' `-^ `-' |\     | `-^ `-' |\         
                            ' ` /  |         ' `        
                                `--'                    
                                 
                               ''')
    bet = get_bet(wallet)
    if bet == 'q':
        print("\nThanks for playing!\n")
        break
    
    wallet -= bet
    
    # Reset and shuffle the deck
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    deck = [(card, card_values[card]) for card in deck]
    random.shuffle(deck)

    # Deal initial hands
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Round loop
    while True:
        print(f"\nYour hand: {display_hand(player_hand)} = {calculate_hand(player_hand)}\n")
        print(f"Dealer's hand: {display_hand(dealer_hand, hide_first=True)}\n")
        
        player_total = calculate_hand(player_hand)
        if player_total == 21 and len(player_hand) == 2:  # Check for a natural blackjack
            blackjack_payout = bet * 1.5  # Calculate 3:2 payout
            wallet += bet + blackjack_payout  # Return original bet plus 3:2 payout
            print(r''' 
    
        ,-,---. .              ,-_/                    
         '|___/ |  ,-. ,-. . , '  | ,-. ,-. . ,        
-- -- -- ,|   \ |  ,-| |   |/     | ,-| |   |/ -- -- --
        `-^---' `' `-^ `-' |\     | `-^ `-' |\         
                           ' ` /  |         ' `        
                               `--'                    
         .  .          ,.   ,   ,.             
         |  | ,-. . .  `|  /|  / . ,-.         
-- -- -- |  | | | | |   | / | /  | | | -- -- --
         `--| `-' `-'   `'  `'   ' ' '         
         .- |                                  
         `--'                                                                            
                               
                               ''')
            
            print(f"Blackjack! You win ${blackjack_payout:.2f}")
            print()

            break
        elif player_total > 21:
            print("Bust! You lose.")
            print()
            break
        
        action = input("Do you want to hit or stand?\n \nIf you want to hit, Enter 1: \nIf you want to stand, Enter 2: \n").lower()

        if action == '1':
            player_hand.append(deck.pop())
        elif action == '2':
            # Dealer's turn
            while calculate_hand(dealer_hand) < 15:
                dealer_hand.append(deck.pop())
            
            dealer_total = calculate_hand(dealer_hand)
            print(f"\nYour hand: {display_hand(player_hand)} (Total: {player_total})\n")
            print(f"\nDealer's hand: {display_hand(dealer_hand)} (Total: {dealer_total})\n")
            
            if dealer_total > 21:
                print("Dealer busts! You win!")
                print()
                wallet += bet * 2
            elif dealer_total > player_total:
                print("Dealer wins!")
                print()
            elif dealer_total < player_total:
                print(r'''

         .  .          ,.   ,   ,.             
         |  | ,-. . .  `|  /|  / . ,-.         
-- -- -- |  | | | | |   | / | /  | | | -- -- --
         `--| `-' `-'   `'  `'   ' ' '         
         .- |                                  
         `--'                                  
         ''')
                wallet += bet * 2
            else:
                print("It's a tie!")
                wallet += bet  # Return the original bet
            break
        else:
            print("Invalid input. Please enter '1' for hit or '2' for stand.")

    print(f"Your current wallet: ${wallet}\n")
    if wallet <= 0:
        print()
        print(r'''
                  You've run out of money! 
         ____ ____ _  _ ____    ____ _  _ ____ ____         
__ __ __ | __ |__| |\/| |___    |  | |  | |___ |__/ __ __ __
         |__] |  | |  | |___    |__|  \/  |___ |  \                       
              
         ''')
        print()
        break

print(f"Final wallet balance: ${wallet}")
print()
print()





