#!/usr/bin/env python


f = open('input.txt', 'r')
directions = [x.strip() for x in f.read().split(',')]
headings = ['N', 'E', 'S', 'W']
visited = []

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
        for i in range(1, distance):
            if (x, y + i) in visited:
                print "Found Twice!", x, y + i, abs(x) + abs(y + i)
            visited.append((x, y + i))
        y += distance
    if heading == 'E':
        for i in range(1, distance):
            if (x + i, y) in visited:
                print "Found Twice!", x + i, y, abs(x + i) + abs(y)
            visited.append((x + i, y))
        x += distance
    if heading == 'S':
        for i in range(1, distance):
            if (x, y - i) in visited:
                print "Found Twice!", x, y - i, abs(x) + abs(y - i)
            visited.append((x, y - i))
        y -= distance
    if heading == 'W':
        for i in range(1, distance):
            if (x - i, y) in visited:
                print "Found Twice!", x, y, abs(x - i) + abs(y)
            visited.append((x - i, y))
        x -= distance

print 'Blocks away: %s' % (abs(x) + abs(y))
