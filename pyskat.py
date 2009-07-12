#!/usr/bin/env python

import random
import sys

# CONSTANTS

KARO = 40
HERZ = 60
PIK = 80
KREUZ = 100

BUBE = 11
DAME = 12
KOENIG = 13
ASS = 1

suits = {   PIK:    'Pik',
            KREUZ:  'Kreuz',
            KARO:   'Karo',
            HERZ:   'Herz' }

ranks = {   ASS:    'Ass',
            7:      'Sieben',
            8:      'Acht',
            9:      'Neun',
            10:     'Zehn',
            BUBE:   'Bube',
            DAME:   'Dame',
            KOENIG: 'Koenig' }

points = {  ASS:    11,
            7:      0,
            8:      0,
            9:      0,
            10:     10,
            BUBE:   2,
            DAME:  3,
            KOENIG:   4 }

reizen = {  PIK:    11,
            KREUZ:  12,
            KARO:   9,
            HERZ:   10 }

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
        return "%s %s (%d)" % (suits[self.suit], ranks[self.rank], self.point)

    def __cmp__(self, other):
        # jack
        if self.rank == BUBE and other.rank != BUBE:
            return 1
        elif self.rank == BUBE and other.rank == BUBE:
            if self.suit > other.suit:
                return 1
            else:
                return -1
        # no jack
        else:
            if other.rank == BUBE:
                return -1
            # ace
            if self.rank == ASS and other.rank != ASS:
                return 1
            elif self.rank == ASS and other.rank == ASS:
                return 0
            elif other.rank == ASS:
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

    def isGreater(self, other, trumpf, null=False):
        if not null:
            # trumpf ueber fehl
            if ((self.suit == trumpf or self.rank == BUBE) and
                    other.suit != trumpf and
                    other.rank != BUBE):
                return True

            # beide trumpf
            elif ((self.suit == trumpf or self.rank == BUBE) and
                    (other.suit == trumpf or other.rank == BUBE)):
                # bube ueber normal
                if self.rank == BUBE and other.rank != BUBE:
                    return True
                # besserer bube
                elif ((self.rank == BUBE and other.rank == BUBE) and
                        self.suit > other.suit):
                    return True
                # besserer trumpf
                elif ((self.rank != BUBE and other.rank != BUBE) and
                        self > other):
                    return True
                else:
                    return False

            # beide fehl
            elif (self.suit != trumpf and self.rank != BUBE and
                    other.suit != trumpf and other.rank != BUBE):
                # nicht bedient
                if other.suit != self.suit:
                    return True
                # hoeherer fehl
                elif self > other:
                    return True
                else:
                    return False
            else:
                return False

        else:
            # TODO: nullspiel
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
        print "--> mische Karten"
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
        return "%s (Punkte: %d)" % (self.name, self.points)

    def giveCard(self, card):
        card.own(self)
        self.cards.append(card)

    def printCards(self):
        for card in self.cards:
            print card

    def getMaxReizwert(self):
        jacks = []
        max = 0

        for card in self.cards:
            if card.rank == BUBE:
                jacks.append(card)

        jacks.sort(reverse=True)

        # ohne 4 - spiel 5
        if len(jacks) == 0:
            max = 4
        # mit ...
        elif jacks[0].suit == KREUZ:
            for x in jacks:
                if x.suit == (KREUZ - 20*max):
                    max += 1
                else:
                    break
        # ohne ...
        else:
            max = (KREUZ - jacks[0].suit) / 20

        #print "%s: %d" % (self.name, max+1)
        return max+1

    def getBestSuit(self):
        color = 0
        max = 0

        # TODO: bei gleicher Anzahl die 'bessere' farbe
        #       waehlen
        # finde farbe mit meisten karten
        for suit in range(40, 101, 20):
            i = 0
            for card in self.cards:
                if card.suit == suit and card.rank != BUBE:
                    i += 1
            if i >= max:
                color = suit
                max = i

        #print "%s: %s (%d)" % (self.name, suits[color], max)
        return color

    def reizen(self):
        max = reizen[self.getBestSuit()]*self.getMaxReizwert() 

        print "%s: kann bis %d reizen" % (self.name, max)
        return max

    def doSagen(self, hoerer):
        gehoert = False
        for wert in range(18,20,22,23,24,27,30,33,36,40,44,45,48,50,55,60):
            if wert <= self.reizen():
                print "%s sagt %d" % (self.name, self.gereizt)
                self.gereizt = wert
                gehoert = hoerer.doHoeren(wert)
                # hoerer passt
                if gehoert == False:
                    return self
                else:
                    continue
            # sager reizt nicht (weiter)
            else:
                print "%s sagt PASSE" % self.name
                # sager passt sofort (keine 18)
                if self.gereizt = 0:
                    return None
                # sager passt, hoerer -> sager
                else:
                    return hoerer

    def playStich(self, tisch, trumpf):
        print "%s denkt nach..." % self.name

        # player = vorhand
        if len(tisch) == 0:
            # TODO: intelligente kartenauswahl
            # play random card
            i = random.randint(0, len(self.cards)-1)
            print "%s: %s" % (self.name, str(self.cards[i]))
            tisch.append(self.cards[i])
            del self.cards[i]

        # bedienen
        else:
            possible_cards = []

            # trumpf gespielt
            if tisch[0].suit == trumpf or tisch[0].rank == BUBE:
                for j in self.cards:
                    if j.suit == trumpf or j.rank == BUBE:
                        possible_cards.append(j)

            # fehl gespielt
            else:
                for j in self.cards:
                    if tisch[0].suit == j.suit and j.rank != BUBE:
                        possible_cards.append(j)

            print possible_cards

            # stechen/schmieren
            if len(possible_cards) == 0:
                # TODO: intelligente kartenauswahl
                # play random card
                i = random.randint(0, len(self.cards)-1)
                print "%s: %s" % (self.name, str(self.cards[i]))
                tisch.append(self.cards[i])
                del self.cards[i]
            # bedienen
            else:
                if len(possible_cards) == 1:
                    i = 0
                else:
                    # TODO: intelligente kartenauswahl
                    i = random.randint(0, len(possible_cards)-1)
                print "%s: %s" % (self.name, str(possible_cards[i]))
                tisch.append(possible_cards[i])

                # remove played card from cards
                for z in range(len(self.cards)):
                    if possible_cards[i] == self.cards[z]:
                        del self.cards[z]
                        break

        print "Tisch: ", tisch
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
            print "Error: max. 3 Spieler"

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
            print "Error: 3 Spieler noetig"

    def showSkat(self):
        print "Karten im Skat:"
        for card in self.skat:
            print card
        print 70 * '-'

    def nextRound(self):
        self.round += 1
        self.vorhand = (self.vorhand + 1) % 3
        self.giveCards()

        self.printPlayerCards()
        self.showSkat()

        for player in self.players:
            player.reizen()
    
        print "Vorhand:    %s" % self.players[self.vorhand]
        print "Mittelhand: %s" % self.players[(self.vorhand+1)%3]
        print "Hinterhand: %s" % self.players[(self.vorhand+2)%3]
        print 70 * '-'

        # reizen
        gewinner = self.players[(self.vorhand+1)%3].doSagen(self.players[self.vorhand])
        if gewinner != None:
            gewinner = gewinner.doSagen(self.players[(self.vorhand+2)%3])
        else:
            # TODO: beide passen
            pass


        for i in range(10):
            self.nextStich(60)

    def nextStich(self, trumpf):
        tisch = []
        self.stich += 1
        print "*** Runde %d - Stich %d ***" % (self.round, self.stich)
        print "*** Spiel: %s ***" % suits[trumpf]
        tisch = self.players[self.vorhand].playStich(tisch, None)
        tisch = self.players[(self.vorhand+1)%3].playStich(tisch, None)
        tisch = self.players[(self.vorhand+2)%3].playStich(tisch, None)

        self.vorhand = self.calculatePoints(tisch, None)

    def calculatePoints(self, tisch, trumpf):
        winner = None
        points = 0

        # TODO: correct calculation of winner
        #       implementation of 'trumpf'

        if tisch[0].isGreater(tisch[1], trumpf):
            if tisch[0].isGreater(tisch[2], trumpf):
                winner = tisch[0].owner
            else:
                winner = tisch[2].owner
        else:
            if tisch[1].isGreater(tisch[2], trumpf):
                winner = tisch[1].owner
            else:
                winner = tisch[2].owner

        for card in tisch:
            points += card.point
        
        winner.points += points

        print "%s bekommt den Stich" % winner

        # calculate winner/vorhand index
        for x in range(len(self.players)):
            if winner == self.players[x]:
                return x

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
