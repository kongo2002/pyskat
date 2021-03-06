#!/usr/bin/env python

#  This file is part of pyskat.
#
#  Copyright (C) 2009, 2010 by Gregor Uhlenheuer
#
#  pyskat is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyskat is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with pyskat.  If not, see <http://www.gnu.org/licenses/>.

from pyskatrc import *
import tactics
import random
import gtk
import cairo
import sys
import time

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
        if pos == 0:
            self.human = True
        else:
            self.human = False

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

        #print "%s: %s (%d)" % (self.name, SUITS[color], max)
        return color

    def reizen(self):
        max = REIZEN[self.getBestSuit()]*self.getMaxReizwert()
        rating = tactics.rateCards(self)

        print "%s: kann bis %d reizen (Rating=%d)" % (self.name, max, rating)

        # nur reizen, wenn gutes blatt
        if rating >= 6:
            return max
        else:
            return 0

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
            # TODO: kein ass auswaehlen
            for i in range(2-len(skat)):
                j = 0
                for k in range(len(classes)):
                    if len(classes[k]) > 0:
                        if (len(classes[k]) < len(classes[j]) or
                                len(classes[j]) == 0):
                            if not (len(classes[k]) == 1 and
                                    classes[k][0].rank == ASS):
                                j = k
                classes[j].sort()
                # 10 in den skat, wenn kein ass
                if len(classes[j]) == 2 and classes[j][-1].rank == 10:
                    skat.append(classes[j][-1])
                    del classes[j][-1]
                else:
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
        #       beachte gereizten wert
        return self.getBestSuit()

    def playStich(self, tisch):
        card = None

        if self.human:
            tisch.showPlayerCards(self)
            return

        # player = vorhand
        if len(tisch.stich) == 0:
            print self.cards

            # TODO: intelligente kartenauswahl
            card = tactics.aufspielen(self, tisch)

        # player = mittelhand oder hinterhand
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

            # stechen/schmieren
            if len(possible_cards) == 0:
                print self.cards

                # TODO: intelligente kartenauswahl
                card = tactics.stechenSchmieren(self, tisch)
            # bedienen
            else:
                print possible_cards

                if len(possible_cards) == 1:
                    card = possible_cards[0]
                else:
                    # TODO: intelligente kartenauswahl
                    card = tactics.bedienen(self, tisch, possible_cards)

        tisch.playCard(card)

        # wait a moment
        time.sleep(1)

        # benachrichtigen des naechsten spielers
        # oder naechster stich
        if len(tisch.stich) > 0:
            tisch.players[(self.position+1)%3].playStich(tisch)
        else:
            tisch.vorhand = tisch.calculatePoints()
            tisch.nextStich()

class Tisch:

    def __init__(self, win):
        self.players = []
        self.playedStiche = []
        self.stich = []
        self.skat = []
        self.trumpf = 0
        self.vorhand = 0
        self.handspiel = False
        self.spielmacher = None
        self.state = S_WARTEN
        self.win = win
        self.win.da.connect('expose_event', self.expose)

        self.cardgfx = {}
        for i in [x+y for x in [1,13,12,11,10,9,8,7] for y in [40,60,80,100]]:
            try:
                file = "cards/%d.png" % i
                self.cardgfx[i] = cairo.ImageSurface.create_from_png(file)
            except Exception, e:
                print e.message
                sys.exit(1)

    def click_card(self, widget, event, data):
        if data:
            spieler = data.owner
        else:
            return True

        if not spieler.human or self.state != S_SPIELEN:
            return True

        # muss bedient werden?
        if len(self.stich) > 0:
            possible = []

            # trumpf gespielt
            if self.stich[0].suit == self.trumpf or self.stich[0].rank == BUBE:
                for j in spieler.cards:
                    if j.suit == self.trumpf or j.rank == BUBE:
                        possible.append(j)

            # fehl gespielt
            else:
                for j in spieler.cards:
                    if self.stich[0].suit == j.suit and j.rank != BUBE:
                        possible.append(j)

            if len(possible) > 0:
                correct = False
                for card in possible:
                    if card == data:
                        correct = True
                        break
                if not correct:
                    print "*** Bedienzwang ***"
                    return True

        print "*** %s clicked ***" % data
        self.playCard(data)
        self.showPlayerCards(spieler)

        # benachrichtigen des naechsten spielers
        # oder naechster stich
        if len(self.stich) > 0:
            self.players[(spieler.position+1)%3].playStich(self)
        else:
            self.vorhand = self.calculatePoints()
            self.nextStich()

    def expose(self, widget, event):
        self.cr = widget.window.cairo_create()

        width, height = self.win.get_size()
        height -= 140

        offset_w = width / 2 - 120
        offset_h = height / 2 - 95

        self.cr.set_source_rgb(1, 1, 1)
        self.cr.paint()
        self.cr.set_source_rgb(0, 0, 0)

        pname = lambda x: self.players[x].re and "%s %s" % (self.players[x].name,
                "(Re)") or self.players[x].name

        if self.state == S_SPIELEN:
            self.cr.move_to(width/2, height - 20)
            self.cr.show_text(pname(0))
            self.cr.move_to(50, 50)
            self.cr.show_text(pname(1))
            self.cr.move_to(width - 100, 50)
            self.cr.show_text(pname(2))

            self.cr.move_to(width/2, 10)
            self.cr.show_text("Spiel: %s" % SUITS[self.trumpf])

            for card in self.stich:
                index = card.rank + card.suit
                if card.owner.position == 0:
                    self.cr.set_source_surface(self.cardgfx[index],
                            offset_w+35, offset_h+50)
                elif card.owner.position == 1:
                    self.cr.set_source_surface(self.cardgfx[index],
                            offset_w, offset_h)
                else:
                    self.cr.set_source_surface(self.cardgfx[index],
                            offset_w+70, offset_h-50)
                self.cr.paint()

    def card_button(self, id, callb, data):
        image = gtk.Image()
        eb = gtk.EventBox()
        file = "cards/%d.gif" % id
        try:
            image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(file))
        except Exception, e:
            print e.message
            sys.exit(1)
        eb.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        eb.set_visible_window(False)
        eb.connect('button_press_event', callb, data)
        eb.add(image)
        return eb

    def sortHand(self, player):
        # dirty sorting routine
        # TODO: better sorting algorithm
        for y in range(len(player.cards)):
            for z in range(len(player.cards)):
                i = z
                for k in range(z+1, len(player.cards)):
                    if player.cards[k].isGreater(player.cards[i], self.trumpf):
                        i = k
                if z != i:
                    # swap
                    player.cards[i], player.cards[z] = (player.cards[z],
                            player.cards[i])

    def showPlayerCards(self, player):
        if player.human:
            self.sortHand(player)
            self.win.tab.destroy()
            self.win.tab = gtk.Table(1, 10, True)
            offset = 0
            for card in player.cards:
                self.win.tab.attach(self.card_button(card.rank+card.suit,
                    self.click_card, card), offset, offset+1, 0, 1)
                offset += 1
            self.win.v.pack_start(self.win.tab, False, False, 0)
            self.win.show_all()
            self.expose(self.win.da, None)

    def playCard(self, card):
        print "%s: %s" % (card.owner.name, card)
        self.stich.append(card)

        # remove played card from player
        for i in range(len(self.players)):
            for j in range(len(self.players[i].cards)):
                if self.players[i].cards[j] == card:
                    del self.players[i].cards[j]
                    break

        self.expose(self.win.da, None)

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
        self.state = S_REIZEN

        self.spielmacher = self.players[(vorhand+1)%3].doSagen(self.players[vorhand])
        self.spielmacher = self.spielmacher.doSagen(self.players[(vorhand+2)%3])

        if self.spielmacher.gereizt == 0:
            # pruefen ob hinterhand auch passen will
            if not self.spielmacher.doHoeren(18):
                # TODO: alle passen -> ramsch
                print "Alle Spieler passen. Neue Runde!"
                return False

        print "%s gewinnt das Reizen mit %d Punkten" % (self.spielmacher.name,
                self.spielmacher.gereizt)

        self.state = S_SKAT

        self.handspiel = self.spielmacher.takeSkat(self.skat)
        self.spielmacher.re = True

        self.trumpf = self.spielmacher.spielAnsagen()

        return True

    def nextStich(self):
        if len(self.playedStiche) < 10:
            print "*** Stich %d ***" % (len(self.playedStiche)+1)
            print "*** Spiel: %s ***" % SUITS[self.trumpf]

            # nur die vorhand wird aufgerufen
            # die anderen spieler rufen sich selber auf
            # playCard() wird auch von den spielern selber aufgerufen...
            self.players[self.vorhand].playStich(self)

            # wird vom letzten spieler aufgerufen
            #self.vorhand = self.calculatePoints()
        else:
            self.win.roundSummary(self.spielmacher)

    def calculatePoints(self):
        winner = None
        points = 0

        lastStich = self.playedStiche[len(self.playedStiche)-1]

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

class pyskat(gtk.Window):

    def __init__(self):
        super(pyskat, self).__init__()

        self.set_title('pyskat')
        self.set_size_request(800, 600)
        #self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
        self.set_app_paintable(1)
        self.set_position(gtk.WIN_POS_CENTER)

        self.v = gtk.VBox()

        self.da = gtk.DrawingArea()
        self.v.pack_start(self.da, True, True, 0)

        self.tab = gtk.Table(1, 10, True)
        self.v.pack_start(self.tab, False, False, 0)

        self.startb = gtk.Button('Naechste Runde')
        self.startb.connect('button_press_event', self.nextRound, None)
        self.v.pack_start(self.startb, False, False, 0)

        self.add(self.v)
        self.connect('destroy', gtk.main_quit)
        self.show_all()

        self.deck = Deck()
        self.tisch = Tisch(self)
        self.vorhand = 0
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

    def nextRound(self, widget, event, data):
        self.v.remove(widget)
        self.v.resize_children()
        widget.destroy()

        self.round += 1

        self.deck.shuffle()
        self.tisch.giveCards(self.deck.cards)

        self.printPlayerCards()
        self.showSkat()

        for player in self.tisch.players:
            player.reizen()

        print "Vorhand:    %s" % self.tisch.players[self.vorhand]
        print "Mittelhand: %s" % self.tisch.players[(self.vorhand+1)%3]
        print "Hinterhand: %s" % self.tisch.players[(self.vorhand+2)%3]
        print 70 * '-'

        # alle spieler passen
        if not self.tisch.reizen(self.vorhand):
            for card in self.tisch.skat:
                self.deck.cards.append(card)
            del self.tisch.skat[:]

            for player in self.tisch.players:
                self.deck.cards.extend(player.cards)
                del player.cards[:]

            self.vorhand = (self.vorhand + 1) % 3
            widget.show()
            return True

        self.tisch.state = S_SPIELEN

        self.showSkat()

        self.tisch.nextStich()

        return True

    def roundSummary(self, player):
        self.tisch.state = S_WARTEN

        self.vorhand = (self.vorhand + 1) % 3

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

        spielwert = REIZEN[self.tisch.trumpf] * player.getMaxReizwert()

        kontra_pts = 120 - re_pts

        print 70 * '-'
        print "Runde %d - Spiel: %s" % (self.round, SUITS[self.tisch.trumpf])
        print "%s gereizt bis %d" % (player.name, player.gereizt)

        # spiel gewonnen
        if re_pts > 60:
            print "%s gewinnt mit %d zu %d Punkten" % (player.name,
                    re_pts,
                    kontra_pts)

            # schwarz gewonnen
            if re_pts == 120:
                spielwert += REIZEN[self.tisch.trumpf]*2
            # schneider gewonnen
            elif re_pts > 90:
                spielwert += REIZEN[self.tisch.trumpf]

            # ueberreizt
            if player.gereizt > spielwert:
                print "%s hat %d zu %d Punkte bekommen" % (player.name,
                        re_pts, kontra_pts)
                print "Spiel (%d) ueberreizt - verloren!" % spielwert
                spielwert = player.gereizt * 2
                player.gesamt -= spielwert
                print "%s: - %d Punkte" % (player.name, spielwert)
            else:
                player.gesamt += spielwert
                print "%s: + %d Punkte" % (player.name, spielwert)

        # spiel verloren
        else:
            print "%s verliert mit %d zu %d Punkten" % (player.name,
                    re_pts,
                    kontra_pts)

            # schwarz verloren
            if re_pts == 0:
                spielwert += REIZEN[self.tisch.trumpf]*2
            # schneider verloren
            elif re_pts < 30:
                spielwert += REIZEN[self.tisch.trumpf]

            spielwert *= 2
            player.gesamt -= spielwert
            print "%s: - %d Punkte" % (player.name, spielwert)

        del player.cards[:]

        for spieler in self.tisch.players:
            spieler.re = False
            spieler.gereizt = 0
            spieler.points = 0

            if spieler.human:
                self.tisch.showPlayerCards(spieler)

        self.listPlayers()

        self.startb = gtk.Button('Naechste Runde')
        self.startb.connect('button_press_event', self.nextRound, None)
        self.v.pack_start(self.startb, False, False, 0)
        self.show_all()

def main():

    skat = pyskat()
    skat.addPlayer("Gregor")
    skat.addPlayer("Cuyo")
    skat.addPlayer("Dozo")

    skat.listPlayers()

    gtk.main()

if __name__ == '__main__':
    main()

# vim:et sw=4 sts=4 tw=80:
