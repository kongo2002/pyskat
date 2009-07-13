#!/usr/bin/env python

# Last Change: Jul 13, 2009

def aufspielen(spieler, tisch):
    # eigene fehl bestimmen
    own = []
    for farbe in (range(40, 101, 20) if not tisch.trumpf):
        farb = []
        for card in spieler.cards:
            if card.suit == farbe and card.rank != BUBE:
                farb.append(card)
        own.append(farb)
    # eigene trumpf bestimmen
    own_trumpf = []
    for card in spieler.cards:
        if card.suit == tisch.trumpf or card.rank == BUBE:
            own_trumpf.append(card)


    if len(tisch.playedStiche) > 0:
        # gespielte fehl bestimmen
        played = []
        for farbe in (range(40, 101, 20) if not tisch.trumpf):
            farb = []
            for i in tisch.stiche:
                for j in i:
                    if j.suit == farbe and j.rank != BUBE:
                        farb.append(j)
            played.append(farb)
        # gespielte trumpf bestimmen
        played_trumpf = []
        for i in tisch.stiche:
            for j in i:
                if j.suit == tisch.trumpf or j.rank == BUBE:
                    played_trumpf.append(j)

    else:
        print "Erster Stich"

    if spieler.re == True:
        print "%s (Re) kommt raus" % spieler.name

        # ass spielen, wenn kein trumpf
        ace = None
        for card in spieler.cards:
            if card.rank == ASS and card.suit != tisch.trumpf:
                if ace == None:
                    ace = card
                # wenn mehrere, dann die kuerzeste farbe
                else:

    else:
        print "%s (Kontra) kommt raus" % spieler.name
