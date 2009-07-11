#!/usr/bin/env python

import random
import sys

# CONSTANTS

DIAMONDS = 40
HEARTS = 60
SPADES = 80
CLUBS = 100

JACK = 11
QUEEN = 12
KING = 13
ACE = 1

suits = {   SPADES:     'Spades',
            CLUBS:      'Clubs',
            DIAMONDS:   'Diamonds',
            HEARTS:     'Hearts' }

ranks = {   ACE:    'Ace',
            7:      'Seven',
            8:      'Eight',
            9:      'Nine',
            10:     'Ten',
            JACK:   'Jack',
            QUEEN:  'Queen',
            KING:   'King' }

points = {  ACE:    11,
            7:      0,
            8:      0,
            9:      0,
            10:     10,
            JACK:   2,
            QUEEN:  3,
            KING:   4 }

# CLASSES

class Card:

    def __init__(self, id):
        self.suit = id - id % 20
        self.rank = id % 20
        self.point = points[self.rank]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "%s of %s (%d)" % (ranks[self.rank], suits[self.suit], self.point)

    def __cmp__(self, other):
        # jack
        if self.rank == JACK and other.rank != JACK:
            return 1
        elif self.rank == JACK and other.rank == JACK:
            if self.suit > other.suit:
                return 1
            else:
                return -1
        # no jack
        else:
            if other.rank == JACK:
                return -1
            # ace
            if self.rank == ACE and other.rank != ACE:
                return 1
            elif self.rank == ACE and other.rank == ACE:
                return 0
            elif other.rank == ACE:
                return -1
            # ten
            elif self.rank == 10 and other.rank != 10:
                return 1
            elif self.rank == 10 and other.rank == 10:
                return 0
            elif other.rank == 10:
                return -1
            # others
            elif self.rank > other.rank:
                return 1
            elif self.rank == other.rank:
                return 0
            else:
                return -1

    def compare(self, other, null=False):
        if not null:
            if self > other:
                print "%s greater than %s" % (str(self), str(other))
            elif self < other:
                print "%s less than %s" % (str(self), str(other))
            else:
                print "%s equal with %s" % (str(self), str(other))
        else:
            # TODO
            print "not implemented yet"

class Deck:

    def __init__(self):
        card_range = (1,7,8,9,10,11,12,13)
        self.cards = [Card(x+y) for x in card_range for y in range(40,101,20)]
        self.shuffle()

    def printDeck(self):
        for card in self.cards:
            print card

    def __repr__(self):
        return str(self)

    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s += str(self.cards[i]) + '\n'
        return s

    def shuffle(self):
        print "--> shuffling card deck"
        for i in range(random.randint(2, 5)):
            random.shuffle(self.cards)

class Player:

    def __init__(self, name):
        self.name = name
        self.points = 0
        self.cards = []
        self.gereizt = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Player: %s\t(Points: %d)" % (self.name, self.points)

    def giveCard(self, card):
        self.cards.append(card)

    def printCards(self):
        for card in self.cards:
            print card

class pyskat:

    def __init__(self):
        self.deck = Deck()
        self.round = 0
        self.stich = 0
        self.players = []
        self.skat = []

    def addPlayer(self, name):
        if len(self.players) < 3:
            self.players.append(Player(name))
        else:
            print "Error: max. 3 Players"

    def listPlayers(self):
        print 70 * '-'
        for player in self.players:
            print player
        print 70 * '-'

    def printPlayerCards(self):
        for player in self.players:
            print player
            player.printCards()
            print 70 * '-'

    def giveCards(self):
        if len(self.players) == 3:
            self.deck.shuffle()

            for player in self.players:
                for i in range(3):
                    player.giveCard(self.deck.cards.pop())
            for player in self.players:
                for i in range(4):
                    player.giveCard(self.deck.cards.pop())
            for player in self.players:
                for i in range(3):
                    player.giveCard(self.deck.cards.pop())

            for i in range(2):
                self.skat.append(self.deck.cards.pop())
        else:
            print "Error: 3 Players required"

    def showSkat(self):
        print "Cards in Skat"
        for card in self.skat:
            print card
        print 70 * '-'

    def nextRound():
        self.round += 1
        self.giveCards()

def main():

    skat = pyskat()
    skat.addPlayer("Gregor")
    skat.addPlayer("Cuyo")
    skat.addPlayer("Dozo")

    skat.listPlayers()
    skat.giveCards()
    skat.printPlayerCards()
    skat.showSkat()

if __name__ == '__main__':
    main()
