#!/usr/bin/env python
# Last Change: Jul 19, 2009

KARO = 40
HERZ = 60
PIK = 80
KREUZ = 100

BUBE = 11
DAME = 12
KOENIG = 13
ASS = 1

SUITS = {   PIK:    'Pik',
            KREUZ:  'Kreuz',
            KARO:   'Karo',
            HERZ:   'Herz' }

RANKS = {   ASS:    'Ass',
            7:      'Sieben',
            8:      'Acht',
            9:      'Neun',
            10:     'Zehn',
            BUBE:   'Bube',
            DAME:   'Dame',
            KOENIG: 'Koenig' }

POINTS = {  ASS:    11,
            7:      0,
            8:      0,
            9:      0,
            10:     10,
            BUBE:   2,
            DAME:   3,
            KOENIG: 4 }

REIZEN = {  PIK:    11,
            KREUZ:  12,
            KARO:   9,
            HERZ:   10 }

class Card:

    def __init__(self, id):
        self.suit = id - id % 20
        self.rank = id % 20
        self.point = POINTS[self.rank]
        self.owner = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "%s %s (%d)" % (SUITS[self.suit], RANKS[self.rank], self.point)

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
