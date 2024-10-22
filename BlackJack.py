import random
from colorama import init, Fore, Back, Style
import time

init()


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

# Function to give the option to re-play the game
def replay_game():
    while True:
        game_option = input(f"{Fore.WHITE}\nWould you like to borrow another {Fore.GREEN}$1000{Fore.WHITE} from the bank? (y/n): {Style.RESET_ALL}").lower()
        if game_option == 'y':
            return True
        elif game_option == 'n':
            return False
        else:
            print("Invalid Input. Please enter 'y' for 'yes', or 'n' for 'no'")

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
        print(Fore.WHITE + "Your wallet: " + Fore.GREEN + f"${wallet}" + Fore.WHITE)
        bet = input(Fore.WHITE + "Enter your bet (or q to quit): " + Fore.GREEN + "$")
        print(Fore.WHITE, end='')  # Reset color for subsequent prints
        if bet.lower() == 'q':
            return 'q'
        try:
            bet = int(bet)
            if 0 < bet <= wallet:
                return bet
            print("Invalid bet. Please enter an amount within your wallet balance.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

# Add this new function to display statistics
def display_statistics(stats):
    print(Fore.CYAN + "\n=== Game Statistics ===")
    print(f"Games Played: {stats['games_played']}")
    print(f"Games Won: {stats['games_won']}")
    print(f"Games Lost: {stats['games_lost']}")
    print(f"Blackjacks: {stats['blackjacks']}")
    print(f"Busts: {stats['busts']}")
    
    # Color-coded total profit
    if stats['total_profit'] <= -3000:
        profit_color = Fore.RED + Style.BRIGHT
        print(Fore.RED + Style.BRIGHT + "YOU ARE BROKE!!" + Style.RESET_ALL)  
    elif stats['total_profit'] < 0:
        profit_color = Fore.RED
    elif stats['total_profit'] > 0:
        profit_color = Fore.GREEN
    else: 
        profit_color = Fore.CYAN
    print(f"Total Profit: {profit_color}${stats['total_profit']:.2f}{Fore.CYAN}")
    
    print(f"Biggest Win: ${stats['biggest_win']:.2f}")
    print(f"Biggest Loss: ${stats['biggest_loss']:.2f}")
    
    # Calculate win rate here to ensure it's up to date
    if stats['games_played'] > 0:
        win_rate = (stats['games_won'] / stats['games_played']) * 100
    else:
        win_rate = 0.0
    
    print(f"Win Rate: {win_rate:.2f}%")
    print("========================\n" + Style.RESET_ALL)

# Main game loop
def main_loop():
    global wallet
    
    # Initialize statistics
    stats = {
        'games_played': 0,
        'games_won': 0,
        'games_lost': 0,
        'blackjacks': 0,
        'busts': 0,
        'total_profit': 0,
        'biggest_win': 0,
        'biggest_loss': 0,
        'win_rate': 0.0
    }
    
    while True:
        wallet = 1000
        initial_wallet = wallet
        
        while True:
            print(Fore.BLUE + Style.BRIGHT + r'''
            _ _ _ ____ _    ____ ____ _  _ ____    ___ ____
            | | | |___ |    |    |  | |\/| |___     |  |  |
            |_|_| |___ |___ |___ |__| |  | |___     |  |__|
            ''' + Style.RESET_ALL)
                  
            print(Fore.GREEN + Style.BRIGHT + r''' 
        
                ,-,---. .              ,-_/                    
                 '|___/ |  ,-. ,-. . , '  | ,-. ,-. . ,        
        -- -- -- ,|   \ |  ,-| |   |/     | ,-| |   |/ -- -- --
                `-^---' `' `-^ `-' |\     | `-^ `-' |\         
                                   ' ` /  |         ' `        
                                       `--'                                
            ''' + Style.RESET_ALL)
            bet = get_bet(wallet)
            if bet == 'q':
                display_statistics(stats)
                print("\nThanks for playing!\n")
                time.sleep(60)
            
            stats['games_played'] += 1
            initial_hand_wallet = wallet
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
                print(Fore.LIGHTYELLOW_EX + f"\nYour hand: {display_hand(player_hand)} = {calculate_hand(player_hand)}\n")
                print(f"Dealer's hand: {display_hand(dealer_hand, hide_first=True)}\n" + Style.RESET_ALL)
                
                player_total = calculate_hand(player_hand)
                if player_total == 21 and len(player_hand) == 2:  # Check for a natural blackjack
                    blackjack_payout = bet * 1.5  # Calculate 3:2 payout
                    wallet += bet + blackjack_payout  # Return original bet plus 3:2 payout
                    stats['blackjacks'] += 1
                    stats['games_won'] += 1
                    profit = wallet - initial_hand_wallet
                    stats['total_profit'] += profit
                    stats['biggest_win'] = max(stats['biggest_win'], profit)
                    print(Fore.GREEN + Style.BRIGHT + r''' 
        
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
                                
                                ''' + Style.RESET_ALL)
                    
                    print(Fore.GREEN + Style.BRIGHT + f"Blackjack! You win ${blackjack_payout:.2f}" + Style.RESET_ALL)
                    print()

                    break
                elif player_total > 21:
                    print("Bust! You lose.")
                    print()
                    stats['busts'] += 1
                    stats['games_lost'] += 1
                    loss = initial_hand_wallet - wallet
                    stats['total_profit'] -= loss
                    stats['biggest_loss'] = max(stats['biggest_loss'], loss)
                    break
                
                if len(player_hand) == 2:
                    action = input(Fore.WHITE + f"Do you want to hit, stand, or double down?\n \nIf you want to HIT, {Fore.RED}Enter 1{Fore.WHITE}: \nIf you want to STAND, {Fore.RED}Enter 2{Fore.WHITE}: \nIf you want to DOUBLE DOWN, {Fore.RED}Enter 3{Fore.WHITE}:\n").lower()
                else:
                    action = input(Fore.WHITE + f"Do you want to hit or stand?\n \nIf you want to HIT, {Fore.RED}Enter 1{Fore.WHITE}: \nIf you want to STAND, {Fore.RED}Enter 2{Fore.WHITE}:\n").lower()

                if action == '1':
                    player_hand.append(deck.pop())
                elif action == '2':
                    # Dealer's turn
                    while calculate_hand(dealer_hand) < 15:
                        dealer_hand.append(deck.pop())
                    
                    dealer_total = calculate_hand(dealer_hand)
                    print(Fore.LIGHTYELLOW_EX + f"\nYour hand: {display_hand(player_hand)} (Total: {player_total})")
                    print(f"\nDealer's hand: {display_hand(dealer_hand)} (Total: {dealer_total})" + Style.RESET_ALL)
                    
                    if dealer_total > 21:
                        print("\nDealer busts! You win!")
                        print()
                        wallet += bet * 2
                        stats['games_won'] += 1
                        profit = wallet - initial_hand_wallet
                        stats['total_profit'] += profit
                        stats['biggest_win'] = max(stats['biggest_win'], profit)
                    elif dealer_total > player_total:
                        print("\nDealer wins!")
                        print()
                        stats['games_lost'] += 1
                        loss = initial_hand_wallet - wallet
                        stats['total_profit'] -= loss
                        stats['biggest_loss'] = max(stats['biggest_loss'], loss)
                    elif dealer_total < player_total:
                        print(Fore.GREEN + Style.BRIGHT + r'''
             .  .          ,.   ,   ,.             
             |  | ,-. . .  `|  /|  / . ,-.         
    -- -- -- |  | | | | |   | / | /  | | | -- -- --
             `--| `-' `-'   `'  `'   ' ' '         
             .- |                                  
             `--'                                  
            ''' + Style.RESET_ALL)
                        wallet += bet * 2
                        stats['games_won'] += 1
                        profit = wallet - initial_hand_wallet
                        stats['total_profit'] += profit
                        stats['biggest_win'] = max(stats['biggest_win'], profit)
                    else:
                        print("\nIt's a tie!")
                        wallet += bet  # Return the original bet
                    break
                elif action == '3' and len(player_hand) == 2:
                    if wallet >= bet:
                        wallet -= bet
                        bet *= 2
                        player_hand.append(deck.pop())
                        print(Fore.LIGHTYELLOW_EX + f"\nYour hand after doubling down: {display_hand(player_hand)} = {calculate_hand(player_hand)}\n" + Style.RESET_ALL)
                        if calculate_hand(player_hand) > 21:
                            print("Bust! You lose.")
                            print()
                            stats['busts'] += 1
                            stats['games_lost'] += 1
                            loss = initial_hand_wallet - wallet
                            stats['total_profit'] -= loss
                            stats['biggest_loss'] = max(stats['biggest_loss'], loss)
                            break
                        # Proceed to dealer's turn
                        while calculate_hand(dealer_hand) < 15:
                            dealer_hand.append(deck.pop())
                        
                        dealer_total = calculate_hand(dealer_hand)
                        print(Fore.LIGHTYELLOW_EX + f"\nYour hand: {display_hand(player_hand)} (Total: {calculate_hand(player_hand)})")
                        print(f"\nDealer's hand: {display_hand(dealer_hand)} (Total: {dealer_total})" + Style.RESET_ALL)
                        
                        if dealer_total > 21:
                            print("\nDealer busts! You win!")
                            print()
                            wallet += bet * 2
                            stats['games_won'] += 1
                            profit = wallet - initial_hand_wallet
                            stats['total_profit'] += profit
                            stats['biggest_win'] = max(stats['biggest_win'], profit)
                        elif dealer_total > calculate_hand(player_hand):
                            print("\nDealer wins!")
                            print()
                            stats['games_lost'] += 1
                            loss = initial_hand_wallet - wallet
                            stats['total_profit'] -= loss
                            stats['biggest_loss'] = max(stats['biggest_loss'], loss)
                        elif dealer_total < calculate_hand(player_hand):
                            print(Fore.GREEN + "\nYou win!" + Style.RESET_ALL)
                            wallet += bet * 2
                            stats['games_won'] += 1
                            profit = wallet - initial_hand_wallet
                            stats['total_profit'] += profit
                            stats['biggest_win'] = max(stats['biggest_win'], profit)
                        else:
                            print("\nIt's a tie!")
                            wallet += bet  # Return the original bet
                        break
                    else:
                        print(Fore.WHITE + "Not enough money to double down. Please choose hit or stand." + Style.RESET_ALL)
                else:
                    print(Fore.WHITE + "Invalid input. Please enter '1' for hit, '2' for stand, or '3' for double down (if applicable)." + Style.RESET_ALL)

            print("Your current wallet:" , end=' ')
            print(Fore.GREEN + Style.BRIGHT + f'${wallet}\n' + Style.RESET_ALL)
            if wallet <= 0 or (stats['total_profit'] <= (-3000)):
                print()
                print(Fore.RED + Style.BRIGHT + r'''
                        You've run out of money! 
                 ____ ____ _  _ ____    ____ _  _ ____ ____         
        __ __ __ | __ |__| |\/| |___    |  | |  | |___ |__/ __ __ __
                 |__] |  | |  | |___    |__|  \/  |___ |  \                       
                    
                ''' + Style.RESET_ALL)
                print()
                break

        print("Final wallet balance:" , end=' ')
        print(Fore.GREEN + Style.BRIGHT + f'${wallet}' + Style.RESET_ALL)
        print()
        
        # Update win rate with debug information
        # print(f"Debug: Games won: {stats['games_won']}, Games played: {stats['games_played']}")
        # stats['win_rate'] = (stats['games_won'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0.0
        # print(f"Debug: Calculated win rate: {stats['win_rate']:.2f}%")
        
        # Display statistics
        display_statistics(stats)
        if stats['total_profit'] <= -3000:
            print(Fore.RED + Style.BRIGHT + r'''
                        You've run out of money! 
                 ____ ____ _  _ ____    ____ _  _ ____ ____         
        __ __ __ | __ |__| |\/| |___    |  | |  | |___ |__/ __ __ __
                 |__] |  | |  | |___    |__|  \/  |___ |  \                       
                    
''' + Style.RESET_ALL)
            break
        
        if not replay_game():
            break
    print()        
    print("Thanks for playing!")
    print()
    time.sleep(60)

init()
main_loop()









