#!/usr/bin/env python

codes = [line.rstrip('\n') for line in open('input.txt')]


KEYPAD = [1, 2, 3,
          4, 5, 6,
          7, 8, 9]

current_index = 4  # we start at 5

for code in codes:
    for move in code:
        if move == "U":
            if current_index - 3 >= 0:
                current_index = current_index - 3
        if move == "R":
            if current_index not in [2, 5, 8]:
                current_index = current_index + 1
        if move == "D":
            if current_index + 3 < 9:
                current_index = current_index + 3
        if move == "L":
            if current_index not in [0, 3, 6]:
                current_index = current_index - 1

    print KEYPAD[current_index]
