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
        self.owner = None

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

    def own(self, player):
        self.owner = player

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
        return "%s\t(Points: %d)" % (self.name, self.points)

    def giveCard(self, card):
        card.own(self)
        self.cards.append(card)

    def printCards(self):
        for card in self.cards:
            print card

    def playStich(self, tisch, trumpf):
        print "Tisch: ",
        print tisch
        print "%s thinking..." % self.name

        # player = vorhand
        if len(tisch) == 0:
            # play random card
            i = random.randint(0, len(self.cards))
            print "%s: %s" % (self.name, str(self.cards[i]))
            tisch.append(self.cards[i])
            del self.cards[i]

        # bedienen
        else:
            possible_cards = []
            for j in self.cards:
                if tisch[0].suit == j.suit:
                    possible_cards.append(j)

            print possible_cards

            # stechen/schmieren
            if len(possible_cards) == 0:
                # play random card
                i = random.randint(0, len(self.cards))
                print "%s: %s" % (self.name, str(self.cards[i]))
                tisch.append(self.cards[i])
                del self.cards[i]
            # bedienen
            else:
                i = random.randint(0, len(possible_cards))
                print "%s: %s" % (self.name, str(possible_cards[i]))
                tisch.append(possible_cards[i])

                # remove played card from cards
                for z in range(len(self.cards)):
                    if possible_cards[i] == self.cards[z]:
                        del self.cards[z]
                        break
        return tisch

class pyskat:

    def __init__(self):
        self.deck = Deck()
        self.round = 0
        self.stich = 0
        self.players = []
        self.skat = []
        self.vorhand = 0

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
        print "Cards in Skat:"
        for card in self.skat:
            print card
        print 70 * '-'

    def nextRound(self):
        self.round += 1
        self.vorhand = (self.vorhand + 1) % 3
        self.giveCards()

        self.printPlayerCards()
        self.showSkat()
    
        print "Vorhand: %s" % self.players[self.vorhand]
        print "Mittelhand: %s" % self.players[(self.vorhand+1)%3]
        print "Hinterhand: %s" % self.players[(self.vorhand+2)%3]
        print 70 * '-'

        for i in range(12):
            self.nextStich()

    def nextStich(self):
        tisch = []
        self.stich += 1
        print "Round %d - Stich %d" % (self.round, self.stich)
        tisch = self.players[self.vorhand].playStich(tisch, None)
        tisch = self.players[(self.vorhand+1)%3].playStich(tisch, None)
        tisch = self.players[(self.vorhand+2)%3].playStich(tisch, None)

        self.vorhand = self.calculatePoints(tisch, None)

    def calculatePoints(self, tisch, trumpf):
        # TODO
        pass

    def reizen(self):
        # TODO
        pass

    def geben(self):
        # TODO
        pass

    def hoeren(self):
        # TODO
        pass

    def sagen(self):
        # TODO
        pass

def main():

    skat = pyskat()
    skat.addPlayer("Gregor")
    skat.addPlayer("Cuyo")
    skat.addPlayer("Dozo")

    skat.listPlayers()

    skat.nextRound()

if __name__ == '__main__':
    main()
