#!/usr/bin/env python


f = open('input.txt', 'r')
directions = [x.strip() for x in f.read().split(',')]
headings = ['N', 'E', 'S', 'W']

x = 0
y = 0
heading = 'N'

for direction in directions:
    turn = direction[0]
    distance = int(direction[1:])
    heading_index = headings.index(heading)
    if turn == 'R':
        heading_index += 1
        if heading_index > len(headings) - 1:
            heading_index = 0
        heading = headings[heading_index]
    if turn == 'L':
        heading_index -= 1
        if heading_index < 0:
            heading_index = len(headings) - 1
        heading = headings[heading_index]

    if heading == 'N':
        y += distance
    if heading == 'E':
        x += distance
    if heading == 'S':
        y -= distance
    if heading == 'W':
        x -= distance

print 'Blocks away: %s' % (abs(x) + abs(y))
