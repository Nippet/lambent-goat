from GameClasses import *


def setup_round(game_deck, player_bal):
    """
    Takes the game deck and player balance and setups up the round including requesting bet
    :param game_deck: Current deck in play
    :param player_bal: Current player balance
    :return: Player hand, computer hand and bet
    """
    player_hand = PlayerHand(game_deck)
    print("Your hand has been drawn")
    print(player_hand)
    print("Computer's hand has been dealt")
    comp_hand = ComputerHand(game_deck)
    bet = player_bal.ask_player_bet()
    return player_hand, comp_hand, bet


def ask_player_action():
    """
    Asks if the player wants to hit or stand
    :return: The inputted player action
    """
    trigger = True
    while trigger:
        action = input("Please enter whether you would like to hit (h) or stand (s): ")
        if action.upper() not in ['H', 'S']:
            print("It looks like you did not enter h or s")
            continue
        else:
            full_action = 'Hit' if action.upper() == 'H' else 'Stand'
            print(f"Player has decided to {full_action}")
            trigger = False
            return action


def check_player_game_state(player_hand):
    """
    Checks for a player win or bust or continue
    :param player_hand: PlayerHand class
    :return: String outcome and relevant score
    """
    if player_hand.best_score > 21:
        bust_amount = player_hand.best_score
        return 'Bust', str(bust_amount)
    elif player_hand.best_score == 21:
        return 'Win', '21'
    else:
        return 'Continue', str(player_hand.best_score)


def check_computer_game_state(comp_hand, player_bal):
    """
    Checks for a computer win or bust
    :param comp_hand: ComputerHand class
    :param player_bal: PlayerBalance class
    :return: True if win or bust, else returns false
    """
    if comp_hand.best_score > 21:
        bust_amount = comp_hand.best_score
        print("Computer has busted!")
        print(f"Computer total is {bust_amount}")
        player_bal.win(player_bal.current_bet * 2)
        balance = player_bal.current_balance
        print(f"Your current balance is now {balance}")
        return True
    elif comp_hand.best_score == 21:
        print("Computer has won!")
        print("Computer total is 21")
        return True
    else:
        return False


def reveal_computer_hand(comp_hand):
    """
    Action to reveal the computers full hand
    :param comp_hand: ComputerHand class
    :return:
    """
    print("Computer will now reveal it's full hand")
    print(comp_hand)


def computer_action(comp_hand, player_hand, deck, player_bal):
    """
    Controls computer actions to get to at least 17
    :param comp_hand: Computer's hand
    :param player_hand: Player's hand
    :param deck: Current deck in play
    :param player_bal: Current balance
    :return:
    """
    loop_end = False
    while not loop_end:
        if comp_hand.best_score >= 17:
            print("Computer will now stand")
            computer_stand(comp_hand, player_hand, player_bal)
            break
        else:
            comp_hand.hit_hand(deck)
            loop_end = check_computer_game_state(comp_hand, player_bal)
    confirm_next_round(player_bal)


def computer_stand(comp_hand, player_hand, player_bal):
    """
    If computer gets to a stand position, determines outcome of round
    :param comp_hand: Computer's hand
    :param player_hand: Player's hand
    :param player_bal: Current balance
    :return:
    """
    if comp_hand.best_score > player_hand.best_score:
        print("Computer has won")
        print("Computer score is: " + str(comp_hand.best_score))
        print("Player score is: " + str(player_hand.best_score))
    elif comp_hand.best_score == player_hand.best_score:
        print("Tied game")
        print("Tied score is: " + str(comp_hand.best_score))
    else:
        print("Computer score is: " + str(comp_hand.best_score))
        print("Player has won")
        player_bal.win(player_bal.current_bet * 2)
        balance = player_bal.current_balance
        print(f"Your current balance is now {balance}")


def player_round(player_hand, comp_hand, player_bal, game_deck):
    """
    Asks player whether they want to hit or stand, and checks for turn exit conditions
    :param player_hand: Current player hand
    :param comp_hand: Current computer's hand
    :param player_bal: Current player balance
    :param game_deck: Current game deck in play
    :return:
    """
    action = ''
    outcome = 'Continue'
    score = ''

    while action.upper() != 'S' and outcome == 'Continue':
        action = ask_player_action()
        if action.upper() == 'H':
            player_hand.hit_hand(game_deck)
            outcome, score = check_player_game_state(player_hand)
        elif action.upper() == 'S':
            score = player_hand.best_score
            break

    if outcome == 'Win':
        print("Player has won!")
        print(f"Player total is {score}")
        player_bal.win(player_bal.current_bet*2)
        balance = player_bal.current_balance
        print(f"Your current balance is now {balance}")
        return False
    elif outcome == 'Bust':
        print("Player has busted!")
        print(f"Unfortunately player total is {score}")
        return False
    else:
        # Player has chosen to stand
        print(f"Your current best score is: {score}")
        reveal_computer_hand(comp_hand)
        return True


def round_cycle(player_bal):
    """
    Standard round actions - player first and then computer
    :param player_bal: Current player balance
    :return:
    """
    game_deck = CardDeck()

    # Draw player and computer hands, assign to variable and ask for bet
    player_hand, comp_hand, bet = setup_round(game_deck, player_bal)

    # Round actions until win, tie or bust
    player_turn_outcome = player_round(player_hand, comp_hand, player_bal, game_deck)
    if player_turn_outcome:
        computer_action(comp_hand, player_hand, game_deck, player_bal)
    else:
        confirm_next_round(player_bal)


def confirm_next_round(player_bal):
    """
    Checks if player has run out of money or if they want to continue playing
    :param player_bal: Current player balance
    :return:
    """
    if player_bal.current_balance == 0:
        print("Sorry you have run out of money. Game over.")
    else:
        response = input("Do you want to keep playing? ")
        while response.upper() not in ('Y', 'N'):
            try:
                print("Please type (y) or (n)")
                continue
            except:
                break
        if response.upper() == 'Y':
            round_cycle(player_bal)
        else:
            print("End game.")
