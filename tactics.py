#!/usr/bin/env python
# Last Change: Jul 14, 2009

from pyskatrc import *

def fehl(trumpf):
    return [x for x in [KARO, HERZ, PIK, KREUZ] if x != trumpf]

def splitCards(cards, trumpf):
    dic = {}
    # fehl karten aufsplitten
    for farbe in fehl(trumpf):
        clist = []
        for card in cards:
            if card.suit == farbe and card.rank != BUBE:
                clist.append(card)
        clist.sort(reverse=True)
        dic[farbe] = clist
    # trumpf aufsplitten
    clist = []
    for card in cards:
        if card.suit == trumpf or card.rank == BUBE:
            clist.append(card)
    clist.sort(reverse=True)
    dic[trumpf] = clist
    return dic

def aufspielen(spieler, tisch):
    # eigene karten 
    own = {}
    own = splitCards(spieler.cards, tisch.trumpf)

    # gespielte karten
    played = {}
    if len(tisch.playedStiche) > 0:
        clist = []
        for stiche in tisch.playedStiche:
            clist.extend(stiche)
        played = splitCards(clist, tisch.trumpf)

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
    for farbe in fehl(tisch.trumpf):
        if len(own[farbe]) < count and len(own[farbe]) != 0:
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
            if tisch.stich[0].isGreater(tisch.stich[1], tisch.trumpf):
                highest = tisch.stich[0]
            else:
                highest = tisch.stich[1]
            # versuche drueber zu kommen
            wahl = None
            for card in possible:
                if card.isGreater(highest, tisch.trumpf):
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
                if card.isGreater(tisch.stich[0], tisch.trumpf):
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
            if tisch.stich[0].isGreater(tisch.stich[1], tisch.trumpf):
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
                    if card.isGreater(highest, tisch.trumpf):
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
            # TODO: wo sitzt Partner?
            # versuche stich zu bekommen
            wahl = None
            for card in possible:
                if card.isGreater(tisch.stich[0], tisch.trumpf):
                    wahl = card
                else:
                    break
            if wahl:
                return wahl
            # ansonsten den kleinsten
            else:
                return possible[len(possible)-1]

def stechenSchmieren(spieler, tisch):
    # eigene karten 
    own = {}
    own = splitCards(spieler.cards, tisch.trumpf)

    # gespielte karten
    played = {}
    if len(tisch.playedStiche) > 0:
        clist = []
        for stiche in tisch.playedStiche:
            clist.extend(stiche)
        played = splitCards(clist, tisch.trumpf)

    # spielmacher
    if spieler.re:
        # sitzt hinten
        if len(tisch.stich) == 2:
            # hoechste karte
            if tisch.stich[0].isGreater(tisch.stich[1], tisch.trumpf):
                highest = tisch.stich[0]
            else:
                highest = tisch.stich[1]
            # nicht nur luschen?
            if (tisch.stich[0].points + tisch.stich[1].points) >= 3:
                # versuche drueber zu kommen
                wahl = None
                for card in own[tisch.trumpf]:
                    if card.isGreater(highest, tisch.trumpf):
                        wahl = card
                    else:
                        break
                if wahl:
                    return wahl
            # abwerfen, wenn nur luschen oder nicht drueber kommt
            wahl = None
            for farbe in fehl(tisch.trumpf):
                for card in own[farbe]:
                    # kleinsten fehl aufwaehlen
                    if not wahl or wahl.points > card.points:
                        wahl = card
                    # wenn gleich, farbe stechen
                    elif wahl.points == card.points:
                        if len(own[farbe]) == 1:
                            wahl = card
            # TODO: AI
            # wenn wahl eine 10 oder ass, evtl doch kleinen trumpf
            if not wahl or wahl.rank == 10 or wahl.rank == ASS:
                wahl = own[tisch.trumpf][len(own[tisch.trumpf])-1]
            return wahl
        # sitzt in der mitte
        else:
            # wenn noch truempfe, dann stechen
            if len(own[tisch.trumpf]) > 0:
                # TODO: AI
                # hoechsten trumpf spielen
                return own[tisch.trumpf][0]
            # wenn keine truempfe, abwerfen
            else:
                wahl = None
                for farbe in fehl(tisch.trumpf):
                    for card in own[farbe]:
                        # kleinsten fehl aufwaehlen
                        if not wahl or wahl.points > card.points:
                            wahl = card
                        # wenn gleich, farbe stechen
                        elif wahl.points == card.points:
                            if len(own[farbe]) == 1:
                                wahl = card
                return wahl
