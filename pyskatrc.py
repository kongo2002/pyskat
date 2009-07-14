#!/usr/bin/env python

# Last Change: Jul 14, 2009

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
