# An implementation of Sum Game, to run in your terminal
# Sean Reid

import copy
import random

# Game implements the flow of the game
class Game:
    def __init__(self, num_players):
        self.human = Human()
        self.autoplayers = []
        for ii in range(num_players - 1):
            self.autoplayers.append(AutoPlayer())
        self.reset()
    
    # reset game
    def reset(self):
        self.deck = Deck()
        self.human.score = 0
        self.human.hand = Hand()
        self.human.deal_cards(self.deck, num_cards = 6)
        for ap in self.autoplayers:
            ap.score = 0
            ap.hand = Hand()
            ap.deal_cards(self.deck, num_cards = 6)
    
    # randomly place cards face up from hand
    def setup(self):
        for card in random.sample(self.human.hand.cards, 3):
            card.hidden = False
        for ap in self.autoplayers:
            for card in random.sample(ap.hand.cards, 3):
                card.hidden = False
    
    # used for card swapping
    def get_hands(self):
        hands = []
        hands.append(self.human.hand)
        for ap in self.autoplayers:
            hands.append(ap.hand)
        return hands
    
    # plays the game
    def play(self):
        self.setup()
        while len(self.deck.cards) > 0:
            self.print_game()
            self.human.deal_cards(self.deck, num_cards = 1)
            hands = self.get_hands()
            self.human.swap(hands)
            self.human.discard()
            # self.print_game()
            for ap in self.autoplayers:
                if len(self.deck.cards) <= 0:
                    break
                ap.deal_cards(self.deck, num_cards = 1)
                hands = self.get_hands()
                ap.swap(hands)
                ap.discard()
                # self.print_game()
        self.scoring()

    # calculates the winner (closest hand sum to match hand sums)
    def scoring(self):
        players = [self.human] + self.autoplayers
        for p0 in players:
            md = 1e9
            for p1 in players:
                d = p0.hand.min_diff(p1.hand)
                if d < md:
                    md = d
            p0.score = md
        winning_score = min([p.score for p in players])
        winners = []
        for ii, p in enumerate(players):
            if p.score == winning_score:
                winners.append(ii)
        if 0 in winners:
            winstr = f"You won! The winning score was {winning_score}."
            if len(winners) > 1:
                winstr += " Other winner(s): "
                for w in winners[1:]:
                    winstr += f"BOT {w}, "
                winstr = winstr[:-2]
        else:
            winstr = f"You lost. The winning score was {winning_score}. The winner(s) are: "
            for w in winners:
                winstr += f"BOT {w}, "
            winstr = winstr[:-2]
        print(winstr)

    # print the game state, with the option of revealing all cards
    def print_game(self, reveal=False):
        if reveal:
            self.human.hand.reveal_all()
            for ap in self.autoplayers:
                ap.hand.reveal_all()
        print(str(self))
        if reveal:
            self.human.hand.revert_reveal_all()
            for ap in self.autoplayers:
                ap.hand.revert_reveal_all()

    # displays the game state
    def __str__(self):
        gamestr = "YOUR HAND\n"
        gamestr += f"{self.human.hand}\n\n"
        for ii, ap in enumerate(self.autoplayers):
            gamestr += f"BOT {ii + 1}'S HAND\n"
            gamestr += f"{ap.hand}\n\n"
        return gamestr

# Deck implements a 52 card deck
class Deck:

    suits = ["H", "S", "C", "D"]
    maxnum = 13

    def __init__(self):
        self.init_cards()
        self.shuffle()

    # iterate through all suits and numbers (Ace has value 1) and assign them to the deck
    def init_cards(self):
        self.cards = []
        for suit in self.suits:
            for number in range(1, self.maxnum + 1):
                card = Card(number, suit)
                self.cards.append(card)
    
    # randomize deck
    def shuffle(self):
        random.shuffle(self.cards)

    # draw a card
    def draw(self):
        # Draw card
        card = self.cards.pop()
        return card

# Defines the properties of a card
class Card:

    def __init__(self, number, suit, hidden = True):
        self.number = number
        self.suit = suit
        self.hidden = hidden

    # Displays the card nicely on the terminal
    def __str__(self):
        if self.hidden:
            val = "  "
        elif self.number == 1:
            val = " A"
        elif self.number == 11:
            val = " J"
        elif self.number == 12:
            val = " Q"
        elif self.number == 13:
            val = " K"
        else:
            val = f"{self.number:>2}"
        if self.hidden:
            suit = " "
        elif self.suit == "H":
            suit = "♥"
        elif self.suit == "S":
            suit = "♠"
        elif self.suit == "C":
            suit = "♣"
        elif self.suit == "D":
            suit = "♦"
        return f"-------\n|     |\n|     |\n|     |\n| {val}{suit} |\n|     |\n|     |\n|     |\n-------"

# Base class, extended to AI and Human
class Player:
    def __init__(self):
        self.hand = Hand()

    # Deal card from deck to player
    def deal_cards(self, deck, num_cards):
        for _ in range(num_cards):
            card = deck.draw()
            self.hand.add(card)

# Autoplayer randomly plays the game (pretty good strategy unless you know how to count cards)
class AutoPlayer(Player):
    def __init__(self):
        super().__init__()
    
    # swap a card from your hand with a match hand
    def swap(self, hands):
        pii = random.randint(0, len(hands)-1)
        hand = hands[pii]
        miis = []
        for ii, card in enumerate(hand.cards):
            if not card.hidden:
                miis.append(ii)
        ciis = []
        for ii, card in enumerate(self.hand.cards):
            if card.hidden:
                ciis.append(ii)
        mii = random.randint(1, len(miis))
        cii = random.randint(1, len(ciis))
        # Handle the case if the match hand is in your hand
        if self.hand == hands[pii]:
            self.hand.cards[ciis[cii-1]].hidden = False
            self.hand.cards[miis[mii-1]].hidden = True
        else:
            ap_card = self.hand.cards.pop(ciis[cii-1])
            match_card = hands[pii].cards.pop(miis[mii-1])
            ap_card.hidden = False
            match_card.hidden = True
            self.hand.cards.append(match_card)
            hands[pii].cards.append(ap_card)

    # Discard a card from hand at random
    def discard(self):
        ciis = []
        for ii, card in enumerate(self.hand.cards):
            if card.hidden:
                ciis.append(ii)
        cii = random.randint(1, len(ciis))
        self.hand.cards.pop(ciis[cii-1])

# Interface for a human to play the game with prompts
class Human(Player):
    def __init__(self):
        super().__init__()

    # Prompt player to select cards to swap
    def swap(self, hands):
        ciis = []
        for ii, card in enumerate(self.hand.cards):
            if card.hidden:
                ciis.append(ii)
        human_hand = Hand()
        for ii in ciis:
            human_hand.add(self.hand.cards[ii])
        human_hand.reveal_all()
        print(f"\nYOUR HAND\n{human_hand}\n\n")
        human_hand.revert_reveal_all()
        cii = int(input(f"Choose a card in your hand to swap (1-{len(human_hand.cards)}): "))
        pii = int(input("Choose a player to swap (0 for you): "))
        hand = hands[pii]
        miis = []
        for ii, card in enumerate(hand.cards):
            if not card.hidden:
                miis.append(ii)
        match_hand = Hand()
        for ii in miis:
            match_hand.add(hand.cards[ii])
        print(f"\nCHOSEN HAND\n{match_hand}\n\n")
        mii = int(input(f"Choose a card in chosen match hand to swap (1-{len(match_hand.cards)}): "))
        if self.hand == hands[pii]:
            self.hand.cards[ciis[cii-1]].hidden = False
            self.hand.cards[miis[mii-1]].hidden = True
        else:
            human_card = self.hand.cards.pop(ciis[cii-1])
            match_card = hands[pii].cards.pop(miis[mii-1])
            human_card.hidden = False
            match_card.hidden = True
            self.hand.cards.append(match_card)
            hands[pii].cards.append(human_card)

    # Prompt player to discard a card
    def discard(self):
        ciis = []
        for ii, card in enumerate(self.hand.cards):
            if card.hidden:
                ciis.append(ii)
        human_hand = Hand()
        for ii in ciis:
            human_hand.add(self.hand.cards[ii])
        human_hand.reveal_all()
        print(f"\nYOUR HAND\n{human_hand}\n\n")
        human_hand.revert_reveal_all()
        cii = int(input(f"Choose a card in your hand to discard (1--{len(human_hand.cards)}): "))
        self.hand.cards.pop(ciis[cii-1])

# Hand is a collection of cards equipped with scoring
class Hand:
    def __init__(self):
        self.cards = []
        self.cards_arxiv = []
        self.just_revealed = False

    # Switch state of all cards to revealed, and save a backup in case you want to revert this
    def reveal_all(self):
        if not self.just_revealed:
            self.cards_arxiv = copy.deepcopy(self.cards)
            for card in self.cards:
                card.hidden = False
            self.just_revealed = True

    # Revert the reveal of all cards by referencing the backup
    def revert_reveal_all(self):
        if self.just_revealed:
            for ca in self.cards_arxiv:
                for c in self.cards:
                    if c.suit == ca.suit and c.number == ca.number:
                        c.hidden = ca.hidden
            self.just_revealed = False
    
    # put a new card in the hand
    def add(self, card):
        self.cards.append(card)

    # calculate all possible sums, including branches for different values of Ace.
    def sums(self, match_hand=False):
        sums = [0]
        for card in self.cards:
            if match_hand:
                if card.hidden:
                    continue
            else:
                if not card.hidden:
                    continue
            if card.number == 1:
                sums_tmp = []
                for s in sums:
                    sums_tmp.append(s + 11)
                    sums_tmp.append(s + 1)
                sums = sums_tmp
            else:
                if card.number > 10:
                    value = 10
                else:
                    value = card.number
                for ii, s in enumerate(sums):
                    sums[ii] += value
        return sums

    # Minimum difference between hands.
    def min_diff(self, match_hand):
        d = 1e9
        for s0 in self.sums():
            for s1 in match_hand.sums(True):
                if abs(s1 - s0) < d:
                    d = abs(s1 - s0)
        return d
    
    # Format hand prettily
    def __str__(self):
        handstr = []
        for card in self.cards:
            if card.hidden:
                handstr.append(str(card).split("\n"))
        for card in self.cards:
            if not card.hidden:
                handstr.append(str(card).split("\n"))
        return "\n".join([" ".join(elem) for elem in zip(*handstr)])

# Play game
def main():
    g = Game(num_players = 3)
    g.play()

if __name__ == "__main__":
    main()
