#!/usr/bin/env python
# Last Change: Jul 16, 2009

from pyskatrc import *

def fehl(trumpf):
    return [x for x in [KARO, HERZ, PIK, KREUZ] if x != trumpf]

def smallest(farbe):
    return farbe[-1]

def biggest(farbe):
    return farbe[0]

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

def isHighest(card, played_cards):
    ref = [card.suit+x for x in [ASS,10,KOENIG,DAME,9,8,7]]

    # gespielte karten entfernen
    for pcard in played_cards[card.suit]:
        for ref_card in ref:
            if (pcard.rank+pcard.suit) == ref_card:
                del ref_card
                break

    # zu spielende karte entfernen
    for ref_card in ref:
        if (card.rank+card.suit) == ref_card:
            del ref_card
            break

    if len(ref) == 0:
        return True
    elif POINTS[card.rank] > POINTS[ref[0]%20]:
        return True
    elif POINTS[card.rank] == POINTS[ref[0]%20]:
        if card.rank > (ref[0] - ref[0]%20):
            return True
        else:
            return False
    else:
        return False

def hatGestochen(spieler, tisch, farbe):
    if farbe != tisch.trumpf:
        for stich in tisch.stiche:
            if (stich[0].suit == farbe and stich[0].owner != spieler and
                    stich[0].rank != BUBE):
                if stich[1].owner == spieler:
                    if stich[1].suit != farbe or stich[1].rank == BUBE:
                        return True
                    else:
                        continue
                else:
                    if stich[2].suit != farbe or stich[2].rank == BUBE:
                        return True
                    else:
                        continue
    else:
        for stich in tisch.stiche:
            if ((stich[0].suit == farbe or stich[0].rank == BUBE) and
                    stich[0].owner != spieler):
                if stich[1].owner == spieler:
                    if stich[1].suit != farbe and stich[1].rank != BUBE:
                        return True
                    else:
                        continue
                else:
                    if stich[2].suit != farbe and stich[2].rank != BUBE:
                        return True
                    else:
                        continue

    return False

def rateCards(spieler):
    buben = 0
    max_farbe = 0
    max_fehlass = 0
    farben_stechen = 0

    own = {}
    own = splitCards(spieler.cards, 100)

    for farbe in own:
        if len(own[farbe]) == 0:
            farben_stechen += 1

    for card in spieler.cards:
        if card.rank == BUBE:
            buben += 1
        elif card.suit == spieler.getBestSuit():
            max_farbe += 1
        elif card.rank == ASS:
            max_fehlass += 1

    return buben*1.5+max_farbe+max_fehlass+farben_stechen

def aufspielen(spieler, tisch):
    # eigene karten 
    own = {}
    own = splitCards(spieler.cards, tisch.trumpf)

    # gespielte karten
    played = {}
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
            elif len(own[card.suit]) == 1:
                ace = card
            elif len(played[card.suit]) < len(played[ace.suit]):
                ace = card
    if ace:
        return ace

    # 10 spielen, wenn ass schon raus
    ten = None
    for farbe in fehl(tisch.trumpf):
        if len(own[farbe]) > 0:
            if own[farbe][0].rank == 10:
                if isHighest(own[farbe][0], played):
                    # wenn mehrere, dann kuerzeste
                    if not ten or len(played[farbe]) < len(played[ten.suit]):
                        ten = own[farbe][0]
    if ten:
        return ten

    # spielmacher
    if spieler.re:
        # hohen trumpf spielen
        # TODO: gespielte truempfe einberechnen
        if len(own[tisch.trumpf]) > 0:
            return biggest(own[tisch.trumpf])

    # kurzen fehl spielen
    wahl = None
    for farbe in fehl(tisch.trumpf):
        if ((not wahl or len(own[farbe]) < len(own[wahl])) and
                len(own[farbe]) > 0):
            wahl = farbe
    # TODO: 10 spielen, wenn ass schon raus
    #       stechen/schmieren kalkulieren
    if wahl:
        if isHighest(biggest(own[wahl]), played):
            return biggest(own[wahl])
        else:
            return smallest(own[wahl])

    return biggest(own[tisch.trumpf])


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
                return smallest(possible)
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
                return smallest(possible)
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
                return smallest(possible)
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
                    return smallest(possible)
        # sitzt in der mitte
        else:
            # TODO: wo sitzt Partner?
            # versuche stich zu bekommen
            if possible[0].rank == ASS:
                return possible[0]

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
                return smallest(possible)

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
            if (tisch.stich[0].point + tisch.stich[1].point) >= 3:
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
                    if not wahl or wahl.point > card.point:
                        wahl = card
                    # wenn gleich, farbe stechen
                    elif wahl.point == card.point:
                        if len(own[farbe]) == 1:
                            wahl = card
            # TODO: AI
            # wenn wahl eine 10 oder ass, evtl doch kleinen trumpf
            if not wahl or wahl.rank == 10 or wahl.rank == ASS:
                if len(own[tisch.trumpf]) > 0:
                    wahl = smallest(own[tisch.trumpf])
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
                        if not wahl or wahl.point > card.point:
                            wahl = card
                        # wenn gleich, farbe stechen
                        elif wahl.point == card.point:
                            if len(own[farbe]) == 1:
                                wahl = card
                return wahl
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
                # TODO: AI
                # mit hoechstem fehl schmieren
                wahl = None
                for farbe in fehl(tisch.trumpf):
                    for card in own[farbe]:
                        if not wahl or card.point > wahl.point:
                            wahl = card
                        elif wahl.point == card.point:
                            if len(own[farbe]) == 1:
                                wahl = card
                if wahl:
                    return wahl
                # wenn kein fehl mehr, kleinen trumpf
                else:
                    return smallest(own[tisch.trumpf])
            # ansonsten, versuche stich zu bekommen
            else:
                # wenn noch truempfe, dann stechen
                if len(own[tisch.trumpf]) > 0:
                    # TODO: AI
                    # kleinst noetigsten trumpf spielen
                    wahl = None
                    for card in own[tisch.trumpf]:
                        if card.isGreater(tisch.stich[0], tisch.trumpf):
                            wahl = card
                        else:
                            break
                    if wahl:
                        return wahl
                # wenn keine ausreichenden truempfe, abwerfen
                wahl = None
                for farbe in fehl(tisch.trumpf):
                    for card in own[farbe]:
                        # kleinsten fehl aufwaehlen
                        if not wahl or wahl.point > card.point:
                            wahl = card
                        # wenn gleich, farbe stechen
                        elif wahl.point == card.point:
                            if len(own[farbe]) == 1:
                                wahl = card
                if wahl:
                    return wahl
                else:
                    return smallest(own[tisch.trumpf])
        # sitzt in der mitte
        else:
            # TODO: wo sitzt Partner?
            #       kann der Partner stechen?
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
                        if not wahl or wahl.point > card.point:
                            wahl = card
                        # wenn gleich, farbe stechen
                        elif wahl.point == card.point:
                            if len(own[farbe]) == 1:
                                wahl = card
                return wahl
