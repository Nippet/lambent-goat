import random


class PlayerBalance:
    """
    Tracks the players betting balance and handles bets and wins
    """

    def __init__(self, current_balance=200):
        self.current_balance = current_balance
        self.current_bet = 0
        print(f"Your starting betting balance is {self.current_balance}")

    def bet_amount(self, amount):
        """
        Registers a player bet
        :param amount: The amount to be bet by the player
        :return: False if bet is invalid, otherwise True and updates the player balance
        """
        if amount > self.current_balance:
            return False
        else:
            self.current_balance = self.current_balance - amount
            return True

    def ask_player_bet(self):
        """
        Asks the player to place their bet and checks balance
        :return: The bet amount as an integer
        """
        while True:
            try:
                balance = self.current_balance
                print(f"Your current balance is {balance}")
                bet = int(input("Please enter your bet: "))
            except:
                print("It looks like you did not enter an integer value")
                continue
            else:
                if not self.bet_amount(bet):
                    print("Insufficient funds")
                    continue
                else:
                    self.current_bet = bet
                    print(f"Thank you, your bet of {bet} has been registered")
                    break
        return bet

    def win(self, win_amount):
        """
        Returns the win to the player balance
        :param win_amount: The total amount won by the player
        :return: Updates the player balance
        """
        self.current_balance = self.current_balance + win_amount

    def __str__(self):
        return str(self.current_balance)


class CardDeck:
    """
    The cards within the deck along with shuffling and resetting
    """

    def __init__(self, deck=['']):
        spades = ['AceS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JackS', 'QueenS', 'KingS']
        hearts = ['AceH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JackH', 'QueenH', 'KingH']
        clubs = ['AceC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JackC', 'QueenC', 'KingC']
        diamonds = ['AceD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JackD', 'QueenD', 'KingD']
        deck = spades + hearts + clubs + diamonds
        random.shuffle(deck)
        self.deck = deck
        print("Deck has been created and shuffled")

    def draw_card(self):
        """
        Reveals the top card in the deck and removes it from remaining pile
        :return: Pops the drawn card from the deck
        """
        revealed_card = translate_card(self.deck[-1])
        print(f"{revealed_card} has been drawn")
        self.deck.pop()

    def draw_hand(self):
        """
        Draws a 2 card hand from the deck
        :return: The 2 card hand
        """
        card_for_hand_one = self.deck.pop()
        card_for_hand_two = self.deck.pop()
        hand = [card_for_hand_one, card_for_hand_two]
        return hand

    def draw_for_hit(self):
        """
        Draws one card from the deck when the player requests a hit
        :return: The drawn card
        """
        card_for_hand = self.deck.pop()
        return card_for_hand

    def __str__(self):
        return ' '.join(self.deck)


class PlayerHand:
    """
    The cards in the player's hand
    """
    def __init__(self, deck):
        self.hand = deck.draw_hand()
        self.max_total = self.max_card_total()
        self.min_total = self.min_card_total()
        self.best_score = self.best_card_score()

    def __str__(self):
        return ', '.join(translate_card(self.hand)) + " is in your hand"

    def hit_hand(self, deck):
        """
        Appends the card that was drawn as part of the hit to the hand
        :param deck: The current deck in play
        :return:
        """
        self.hand.append(deck.draw_for_hit())
        drawn_card = self.hand[-1]
        self.max_total = self.max_card_total()
        self.min_total = self.min_card_total()
        self.best_score = self.best_card_score()
        print(f"{translate_card([drawn_card])} was drawn and added to the hand")
        print(self)

    def max_card_total(self):
        """
        Maximum total for the hand - ie considering the value of aces as 1
        :return: The Maximum total for the hand
        """
        card_totals = {'AceS': [1, 11], '2S': 2, '3S': 3, '4S': 4, '5S': 5, '6S': 6, '7S': 7, '8S': 8, '9S': 9, '10S': 10, 'JackS': 10, 'QueenS': 10, 'KingS': 10, \
        'AceH': [1, 11], '2H': 2, '3H': 3, '4H': 4, '5H': 5, '6H': 6, '7H': 7, '8H': 8, '9H': 9, '10H': 10, 'JackH': 10, 'QueenH': 10, 'KingH': 10, \
        'AceC': [1, 11], '2C': 2, '3C': 3, '4C': 4, '5C': 5, '6C': 6, '7C': 7, '8C': 8, '9C': 9, '10C': 10, 'JackC': 10, 'QueenC': 10, 'KingC': 10, \
        'AceD': [1, 11], '2D': 2, '3D': 3, '4D': 4, '5D': 5, '6D': 6, '7D': 7, '8D': 8, '9D': 9, '10D': 10, 'JackD': 10, 'QueenD': 10, 'KingD': 10}
        max_hand_total = 0
        for card in self.hand:
            if 'Ace' in card:
                max_hand_total += card_totals[card][1]
            else:
                max_hand_total += card_totals[card]
        return max_hand_total

    def min_card_total(self):
        """
        Minimum total for the hand - ie considering the value of aces as 1
        :return: The minimum total for the hand
        """
        card_totals = {'AceS': [1, 10], '2S': 2, '3S': 3, '4S': 4, '5S': 5, '6S': 6, '7S': 7, '8S': 8, '9S': 9, '10S': 10, 'JackS': 10, 'QueenS': 10, 'KingS': 10, \
        'AceH': [1, 10], '2H': 2, '3H': 3, '4H': 4, '5H': 5, '6H': 6, '7H': 7, '8H': 8, '9H': 9, '10H': 10, 'JackH': 10, 'QueenH': 10, 'KingH': 10, \
        'AceC': [1, 10], '2C': 2, '3C': 3, '4C': 4, '5C': 5, '6C': 6, '7C': 7, '8C': 8, '9C': 9, '10C': 10, 'JackC': 10, 'QueenC': 10, 'KingC': 10, \
        'AceD': [1, 10], '2D': 2, '3D': 3, '4D': 4, '5D': 5, '6D': 6, '7D': 7, '8D': 8, '9D': 9, '10D': 10, 'JackD': 10, 'QueenD': 10, 'KingD': 10}
        min_hand_total = 0
        for card in self.hand:
            if 'Ace' in card:
                min_hand_total += card_totals[card][0]
            else:
                min_hand_total += card_totals[card]
        return min_hand_total

    def best_card_score(self):
        if self.max_total <= 21:
            return self.max_total
        else:
            return self.min_total


class ComputerHand(PlayerHand):
    """
    The cards in the computer's hand
    """
    def __init__(self, deck):
        PlayerHand.__init__(self, deck)
        print(f"The computer has the following card face up: {translate_card([self.hand[0]])}")

    def __str__(self):
        return ', '.join(translate_card(self.hand)) + " is now in the computer's hand"


def translate_card(shorthand_card):
    """
    Function that converts abbreviated card to full description
    :param shorthand_card: The abbreviated card
    :return: The plain english description of the card
    """
    if len(shorthand_card) == 1:
        translation = ''.join(shorthand_card)
        translation = ((((translation.replace('S', ' of Spades')).replace('H', ' of Hearts'))
                        .replace('C', ' of Clubs')).replace('D', ' of Diamonds'))
    else:
        translation = [((((word.replace('S', ' of Spades')).replace('H', ' of Hearts')).replace('C', ' of Clubs'))
                        .replace('D', ' of Diamonds')) for word in shorthand_card]
    return translation
