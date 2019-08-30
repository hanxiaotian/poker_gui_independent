import random

CARDS2VALUES = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                'K': 13, 'A': 14, '2': 17, 'SJ': 20, 'BJ': 30}
VALUES2CARDS = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q',
                13: 'K', 14: 'A', 17: '2', 20: 'SJ', 30: "BJ"}


class Card:

    def __init__(self, rank, suit):

        self.rank = 0
        self.suit = suit
        self.upward = True

        if rank == 'SJ' or rank == 'BJ':
            self.image_path = 'img/' + rank + '.png'
        elif rank == '2':
            self.image_path = 'img/' + rank + suit + '.png'
        else:
            self.image_path = 'img/' + str(CARDS2VALUES[rank]) + suit + '.png'

        self.rank = CARDS2VALUES[rank]

    def __str__(self):
        if self.rank == 20 or self.rank == 30:
            return VALUES2CARDS[self.rank]
        return VALUES2CARDS[self.rank] + self.suit

    def __eq__(self, other):
        if self.rank == other.rank and self.suit == other.suit:
            return True
        return False


# only exists for the __str__ function
class Hand:

    def __init__(self, hand, deck):
        if isinstance(hand[0], Card):
            self.hand = hand
            return
        self.hand = []
        for v in hand:
            for s in ['H', 'S', 'C', 'D']:
                if v in deck:
                    self.hand.append(deck[v])
                    del deck[v]
                    break
                elif v+s in deck:
                    self.hand.append(deck[v+s])
                    del deck[v+s]
                    break

    def __str__(self):
        out = ""
        for card in self.hand:
            out += str(card) + ", "
        return out

    def __getitem__(self, index):
        return self.hand[index]

    def __len__(self):
        return len(self.hand)

    def remove(self, c):
        self.hand.remove(c)


class Deck:

    def __init__(self):
        self.deck = {}

        for rank in CARDS2VALUES.keys():
            for suit in ['H', 'S', 'C', 'D']:
                if rank not in ('SJ', 'BJ'):
                    self.deck[rank+suit] = Card(rank, suit)
                else:
                    self.deck[rank] = Card(rank, '')
                    break

    def __str__(self):
        out = ""
        for card in self.deck.values():
            out += str(card) + "\n"
        return out

    def __getitem__(self, key):
        return self.deck[key]

    def __contains__(self, key):
        if key in self.deck:
            return True
        return False

    def __delitem__(self, key):
        del self.deck[key]

    def __iter__(self):
        return iter(self.deck.values())

    # return a list a cards taken from the deck
    def deal(self, amount):
        cards = []

        # create and then return a list of cards taken randomly from the deck
        for i in range(amount):
            key, card = random.choice(list(self.deck.items()))
            del self.deck[key]
            cards.append(card)
        return cards
