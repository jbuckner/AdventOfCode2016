#!/usr/bin/env python

CODES = [line.rstrip('\n') for line in open('input.txt')]

A = 'A'
B = 'B'
C = 'C'
D = 'D'

# KEYPAD = [0, 0, 0, 0, 0,
#           0, 1, 2, 3, 0,
#           0, 4, 5, 6, 0,
#           0, 7, 8, 9, 0,
#           0, 0, 0, 0, 0]

KEYPAD = [0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  1,  0,  0,  0,
          0,  0,  2,  3,  4,  0,  0,
          0,  5,  6,  7,  8,  9,  0,
          0,  0,  A,  B,  C,  0,  0,
          0,  0,  0,  D,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0]

WIDTH = 7

current_index = 22  # we start at 5

for code in CODES:
    for move in code:
        if move == "U":
            destination = current_index - WIDTH
        if move == "R":
            destination = current_index + 1
        if move == "D":
            destination = current_index + WIDTH
        if move == "L":
            destination = current_index - 1

        if KEYPAD[destination] != 0:
            current_index = destination

    print KEYPAD[current_index]
