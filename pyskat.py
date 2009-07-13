#!/usr/bin/env python

# Last Change: Jul 13, 2009

import tactics
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
            DAME:   3,
            KOENIG: 4 }

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
            elif self.suit == other.suit:
                return 0
            else:
                return -1
        # no jack
        else:
            if other.rank == BUBE:
                return -1
            # ace
            if self.rank == ASS and other.rank != ASS:
                return 1
            elif (self.rank == ASS and other.rank == ASS and
                    self.suit == other.suit):
                return 0
            elif other.rank == ASS:
                return -1
            # ten
            elif self.rank == 10 and other.rank != 10:
                return 1
            elif (self.rank == 10 and other.rank == 10 and
                    self.suit == other.suit):
                return 0
            elif other.rank == 10:
                return -1
            # others
            elif self.rank > other.rank:
                return 1
            elif (self.rank == other.rank and
                    self.suit == other.suit):
                return 0
            else:
                return -1

    def own(self, player):
        self.owner = player

    def isGreater(self, other, trumpf, null=False):
        if null:
            # TODO: nullspiel (bzw. ramsch)
            pass
        elif not trumpf:
            # TODO: grandspiel
            pass
        else:
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

    def __init__(self, name, pos):
        self.name = name
        self.position = pos
        self.gesamt = 0
        self.points = 0
        self.cards = []
        self.gereizt = 0
        self.re = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "%s (Punkte: %d)" % (self.name, self.gesamt)

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
        # TODO: KI
        #       nicht bis zum maximum reizen
        gehoert = False
        for wert in [18,20,22,23,24,27,30,33,36,40,44,45,48,50,55,60]:
            if self.gereizt > wert:
                continue
            if wert <= self.reizen():
                self.gereizt = wert
                print "%s sagt %d" % (self.name, self.gereizt)
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
                if self.gereizt == 0:
                    return hoerer
                # sager passt, hoerer -> sager
                elif gehoert == True:
                    return hoerer
                # sager passt sofort
                else:
                    if not hoerer.doHoeren(wert):
                        return self
                    else:
                        return hoerer
        return hoerer

    def doHoeren(self, ansage):
        # TODO: KI
        #       nicht bis zum maximum reizen
        if ansage <= self.reizen():
            self.gereizt = ansage
            print "%s sagt JA" % self.name
            return True
        else:
            print "%s sagt PASSE" % self.name
            return False

    def takeSkat(self, skat):
        for x in skat:
            x.own(self)
            self.cards.append(x)
        del skat[:]

        # TODO: KI
        classes = []
        for suit in [40,60,80,100]:
            suited = []
            for card in self.cards:
                if card.suit == suit and card.rank != BUBE:
                    suited.append(card)
            classes.append(suited)

        while len(skat) < 2:
            # nur ein fehl, kein ass
            for farbe in classes:
                print "* %s" % farbe
                if len(skat) < 2 and len(farbe) == 1 and farbe[0].rank != ASS:
                    skat.append(farbe[0])
                    del farbe[0]
                    continue
            # nur zwei fehl, skat noch leer
            if len(skat) == 0:
                for farbe in classes:
                    if (len(farbe) == 2 and farbe[0].rank != ASS and
                            farbe[1].rank != ASS):
                        skat.append(farbe[0])
                        skat.append(farbe[1])
                        del farbe[0]
                        del farbe[0]
                        break
            # rest auswaehlen
            for i in range(2-len(skat)):
                j = 0
                for k in range(len(classes)):
                    if len(classes[k]) > 0:
                        if (len(classes[k]) < len(classes[j]) or
                                len(classes[j]) == 0):
                            j = k
                classes[j].sort()
                skat.append(classes[j][0])
                del classes[j][0]

        # ausgewaehlte karten entfernen
        for card in skat:
            for z in range(len(self.cards)):
                if card == self.cards[z]:
                    del self.cards[z]
                    break

        if len(skat) == 2:
            return False
        else:
            # TODO: handspiel
            return True

    def spielAnsagen(self):
        # TODO: nullspiel und grandspiel
        #       KI
        return self.getBestSuit()

    def playStich(self, tisch):
        print "%s denkt nach..." % self.name

        # player = vorhand
        if len(tisch.stich) == 0:
            # TODO: intelligente kartenauswahl
            # play random card
            #i = random.randint(0, len(self.cards)-1)
            #print "%s: %s" % (self.name, str(self.cards[i]))
            #return self.cards[i]
            return tactics.aufspielen(self, tisch)

        # bedienen
        else:
            possible_cards = []

            # trumpf gespielt
            if tisch.stich[0].suit == tisch.trumpf or tisch.stich[0].rank == BUBE:
                for j in self.cards:
                    if j.suit == tisch.trumpf or j.rank == BUBE:
                        possible_cards.append(j)

            # fehl gespielt
            else:
                for j in self.cards:
                    if tisch.stich[0].suit == j.suit and j.rank != BUBE:
                        possible_cards.append(j)

            possible_cards.sort(reverse=True)
            print possible_cards

            # stechen/schmieren
            if len(possible_cards) == 0:
                # TODO: intelligente kartenauswahl
                # play random card
                i = random.randint(0, len(self.cards)-1)
                #print "%s: %s" % (self.name, str(self.cards[i]))
                return self.cards[i]
            # bedienen
            else:
                if len(possible_cards) == 1:
                    return possible_cards[0]
                else:
                    # TODO: intelligente kartenauswahl
                    #i = random.randint(0, len(possible_cards)-1)
                    return tactics.bedienen(self, tisch, possible_cards)
                #print "%s: %s" % (self.name, str(possible_cards[i]))

        print "Tisch: ", tisch
        return tisch

class Tisch:
    
    def __init__(self):
        self.players = []
        self.playedStiche = []
        self.stich = []
        self.skat = []
        self.trumpf = 0
        self.vorhand = 0
        self.handspiel = False
        self.spielmacher = None

    def playCard(self, card):
        print "%s: %s" % (card.owner.name, card)
        self.stich.append(card)

        # remove played card from player
        for i in range(len(self.players)):
            for j in range(len(self.players[i].cards)):
                if self.players[i].cards[j] == card:
                    del self.players[i].cards[j]
                    break

        if len(self.stich) == 3:
            lastStich = self.stich[:]
            self.playedStiche.append(lastStich)
            del self.stich[:]

    def giveCards(self, cards):
        if len(self.players) == 3:
            # jeweils drei karten geben
            for z in range(3):
                for i in range(3):
                    self.players[(z+self.vorhand)%3].giveCard(cards.pop())
            # skat geben
            for i in range(2):
                self.skat.append(cards.pop())
            # jeweils vier karten geben
            for z in range(3):
                for i in range(4):
                    self.players[(z+self.vorhand)%3].giveCard(cards.pop())
            # jeweils drei karten geben
            for z in range(3):
                for i in range(3):
                    self.players[(z+self.vorhand)%3].giveCard(cards.pop())

        else:
            print "Error: 3 Spieler noetig"

    def reizen(self, vorhand):
        self.spielmacher = self.players[(vorhand+1)%3].doSagen(self.players[vorhand])
        self.spielmacher = self.spielmacher.doSagen(self.players[(vorhand+2)%3])

        if self.spielmacher.gereizt == 0:
            # TODO: alle passen -> ramsch
            pass
        else:
            print "%s gewinnt das Reizen mit %d Punkten" % (self.spielmacher.name,
                    self.spielmacher.gereizt)

            self.handspiel = self.spielmacher.takeSkat(self.skat)
            self.spielmacher.re = True

        self.trumpf = self.spielmacher.spielAnsagen()

    def nextStich(self):
        print "*** Stich %d ***" % (len(self.playedStiche)+1)
        print "*** Spiel: %s ***" % suits[self.trumpf]

        self.playCard(self.players[self.vorhand].playStich(self))
        self.playCard(self.players[(self.vorhand+1)%3].playStich(self))
        self.playCard(self.players[(self.vorhand+2)%3].playStich(self))

        self.vorhand = self.calculatePoints()

    def calculatePoints(self):
        winner = None
        points = 0

        lastStich = self.playedStiche[len(self.playedStiche)-1]

        # TODO: correct calculation of winner
        #       implementation of 'trumpf'

        if lastStich[0].isGreater(lastStich[1], self.trumpf):
            if lastStich[0].isGreater(lastStich[2], self.trumpf):
                winner = lastStich[0].owner
            else:
                winner = lastStich[2].owner
        else:
            if lastStich[1].isGreater(lastStich[2], self.trumpf):
                winner = lastStich[1].owner
            else:
                winner = lastStich[2].owner

        for card in lastStich:
            points += card.point
        
        winner.points += points

        print "%s bekommt den Stich (%d)" % (winner, points)

        # calculate winner/vorhand index
        for x in range(len(self.players)):
            if winner == self.players[x]:
                return x

class pyskat:

    def __init__(self):
        self.deck = Deck()
        self.tisch = Tisch()
        self.round = 0

    def addPlayer(self, name):
        if len(self.tisch.players) < 3:
            self.tisch.players.append(Player(name, len(self.tisch.players)))
        else:
            print "Error: max. 3 Spieler"

    def listPlayers(self):
        print 70 * '-'
        for player in self.tisch.players:
            print player
        print 70 * '-'

    def printPlayerCards(self):
        for player in self.tisch.players:
            print player
            player.printCards()
            print 70 * '-'

    def showSkat(self):
        print "Karten im Skat:"
        for card in self.tisch.skat:
            print card
        print 70 * '-'

    def nextRound(self):
        self.round += 1
        self.tisch.vorhand = (self.tisch.vorhand + 1) % 3

        self.deck.shuffle()
        self.tisch.giveCards(self.deck.cards)

        self.printPlayerCards()
        self.showSkat()

        for player in self.tisch.players:
            player.reizen()
    
        print "Vorhand:    %s" % self.tisch.players[self.tisch.vorhand]
        print "Mittelhand: %s" % self.tisch.players[(self.tisch.vorhand+1)%3]
        print "Hinterhand: %s" % self.tisch.players[(self.tisch.vorhand+2)%3]
        print 70 * '-'

        self.tisch.reizen(self.tisch.vorhand)

        self.showSkat()
        self.printPlayerCards()

        for i in range(10):
            self.tisch.nextStich()

        self.roundSummary(self.tisch.spielmacher)

    def roundSummary(self, player):
        re_pts = player.points
        for card in self.tisch.skat:
            re_pts += card.point
            self.deck.cards.append(card)

        del self.tisch.skat[:]

        # karten zurueck ins deck
        for stich in self.tisch.playedStiche:
            self.deck.cards.extend(stich)
        del self.tisch.playedStiche[:]

        # karten temporaer zurueckholen
        for card in self.deck.cards:
            if card.owner == player:
                player.cards.append(card)

        spielwert = reizen[self.tisch.trumpf] * player.getMaxReizwert()

        kontra_pts = 120 - re_pts

        print 70 * '-'
        print "Runde %d - Spiel: %s" % (self.round, suits[self.tisch.trumpf])
        print "%s gereizt bis %d" % (player.name, player.gereizt)

        # nicht ueberreizt
        if player.gereizt <= spielwert:
            # spiel gewonnen
            if re_pts > 60:
                print "%s gewinnt mit %d zu %d Punkten" % (player.name,
                        re_pts,
                        kontra_pts)

                # schwarz gewonnen
                if re_pts == 120:
                    spielwert += reizen[self.tisch.trumpf]*2
                # schneider gewonnen
                elif re_pts > 90:
                    spielwert += reizen[self.tisch.trumpf]

                player.gesamt += spielwert
                print "%s: + %d Punkte" % (player.name, spielwert)
            # spiel verloren
            else:
                print "%s verliert mit %d zu %d Punkten" % (player.name,
                        re_pts,
                        kontra_pts)

                # schwarz verloren
                if re_pts == 0:
                    spielwert += reizen[self.tisch.trumpf]*2
                # schneider verloren
                elif re_pts < 30:
                    spielwert += reizen[self.tisch.trumpf]

                player.gesamt -= spielwert
                print "%s: - %d Punkte" % (player.name, spielwert)
        # ueberreizt
        else:
            print "Spiel (%d) ueberreizt - verloren!" % spielwert
            spielwert = player.gereizt * 2
            player.gesamt -= spielwert
            print "%s: - %d Punkte" % (player.name, spielwert)

        del player.cards[:]

        for spieler in self.tisch.players:
            spieler.re = False
            spieler.gereizt = 0
            spieler.points = 0

        self.listPlayers()

def main():

    skat = pyskat()
    skat.addPlayer("Gregor")
    skat.addPlayer("Cuyo")
    skat.addPlayer("Dozo")

    skat.listPlayers()

    for i in range(2):
        skat.nextRound()

if __name__ == '__main__':
    main()
