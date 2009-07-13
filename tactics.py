#!/usr/bin/env python

# Last Change: Jul 13, 2009

KARO = 40
HERZ = 60
PIK = 80
KREUZ = 100

BUBE = 11
DAME = 12
KOENIG = 13
ASS = 1

def fehl(trumpf):
    return [x for x in [KARO, HERZ, PIK, KREUZ] if x != trumpf]

def splitCards(cards, trumpf):
    dict = {}
    # fehl karten aufsplitten
    for farbe in fehl(trumpf):
        list = []
        for card in cards:
            if card.suit == farbe and card.rank != BUBE:
                list.append(card)
        list.sort(reverse=True)
        dict[farbe] = list
    # trumpf aufsplitten
    list = []
    for card in cards:
        if card.suit == trumpf or card.rank == BUBE:
            list.append(card)
    list.sort(reverse=True)
    dict[trumpf] = list
    return dict

def aufspielen(spieler, tisch):
    # eigene karten 
    own = {}
    own = splitCards(spieler.cards, tisch.trumpf)

    # gespielte karten
    played = {}
    if len(tisch.playedStiche) > 0:
        list = []
        for stiche in tisch.playedStiche:
            list.extend(stiche)
        played = splitCards(list, tisch.trumpf)

    if spieler.re == True:
        print "%s (Re) kommt raus" % spieler.name
    else:
        print "%s (Kontra) kommt raus" % spieler.name

    # ass spielen, wenn kein trumpf
    ace = None
    for card in spieler.cards:
        if card.rank == ASS and card.suit != tisch.trumpf:
            if not ace:
                ace = card
            # wenn mehrere, dann die kuerzeste farbe
            else:
                # TODO
                pass
    if ace:
        return ace

    # kurzen fehl spielen
    count = 12
    to_play = 0
    for farbe in own:
        if len(own[farbe]) < 12 and len(own[farbe]) != 0:
            to_play = farbe
    # TODO: 10 spielen, wenn ass schon raus
    #       stechen/schmieren kalkulieren
    if to_play:
        return own[to_play][0]

    # hohen trumpf spielen
    # TODO: gespielte truempfe einberechnen
    return own[tisch.trumpf][0]

def bedienen(spieler, tisch, possible):
    # spielmacher
    if spieler.re:
        # sitzt hinten
        if len(tisch.stich) == 2:
            # hoechste karte
            if spieler.isGreater(tisch.stich[0], tisch.stich[1], tisch.trumpf):
                highest = tisch.stich[0]
            else:
                highest = tisch.stich[1]
            # versuche drueber zu kommen
            wahl = None
            for card in possible:
                if isGreater(card, highest):
                    wahl = card
                else:
                    break
            if wahl:
                return wahl
            # ansonsten den kleinsten
            else:
                return possible[len(possible)-1]
        # sitzt in der mitte
        else:
            # versuche stich zu bekommen
            wahl = None
            for card in possible:
                if isGreater(card, tisch.stich[0]):
                    wahl = card
                else:
                    break
            if wahl:
                return wahl
            # ansonsten den kleinsten
            else:
                return possible[len(possible)-1]
    # kontra
    else:
        # sitzt hinten
        if len(tisch.stich) == 2:
            # hoechste karte
            if spieler.isGreater(tisch.stich[0], tisch.stich[1], tisch.trumpf):
                highest = tisch.stich[0]
            else:
                highest = tisch.stich[1]
            # partner hat den stich
            if not highest.owner.re:
                # kleinsten nehmen
                # TODO: AI
                return possible[len(possible)-1]
            # ansonsten, versuche stich zu bekommen
            else:
                wahl = None
                for card in possible:
                    if isGreater(card, highest):
                        wahl = card
                    else:
                        break
                if wahl:
                    return wahl
                # ansonsten den kleinsten
                else:
                    return possible[len(possible)-1]
        # sitzt in der mitte
        else:
            # versuche stich zu bekommen
            wahl = None
            for card in possible:
                if isGreater(card, tisch.stich[0]):
                    wahl = card
                else:
                    break
            if wahl:
                return wahl
            # ansonsten den kleinsten
            else:
                return possible[len(possible)-1]

