#!/usr/bin/env python

import sys

INPUT = 1352
WIDTH = 50
HEIGHT = 50


def is_open_space((x, y)):
    calc = x * x + 3 * x + 2 * x * y + y + y * y
    calc += INPUT
    binary = '{0:b}'.format(calc)
    evens = 0
    for char in list(binary):
        evens += int(char)
    return evens % 2 == 0


def print_board(prior_moves):
    sys.stdout.write('\n  ')
    for x in range(0, WIDTH):
        sys.stdout.write('%s ' % x)
    sys.stdout.write('\n')

    for y in range(0, HEIGHT):
        sys.stdout.write('%s ' % y)

        for x in range(0, WIDTH):
            marker = '.' if is_open_space((x, y)) else '#'
            if (x, y) in prior_moves:
                marker = 'o'

            sys.stdout.write('%s ' % marker)

        sys.stdout.write('\n')

done = False

target_x = 7
target_y = 4

target_coord = (target_x, target_y)

current_x = 1
current_y = 1

# moves = 0

# visited = set()

def make_move(new_coord, last_coord, prior_moves, moves, depth):
    if moves > depth:
        # print 'TOO DEEP', moves, depth
        return False

    # print 'make_move', new_coord, prior_moves
    if new_coord == target_coord:
        print 'FOUND!', moves
        print_board(prior_moves)
        return True

    prior_moves.add(new_coord)

    up_coord = (new_coord[0], new_coord[1] - 1)
    down_coord = (new_coord[0], new_coord[1] + 1)
    left_coord = (new_coord[0] - 1, new_coord[1])
    right_coord = (new_coord[0] + 1, new_coord[1])

    new_up_state = set(prior_moves)
    new_up_state.add(up_coord)
    new_down_state = set(prior_moves)
    new_down_state.add(down_coord)
    new_left_state = set(prior_moves)
    new_left_state.add(left_coord)
    new_right_state = set(prior_moves)
    new_right_state.add(right_coord)

    can_go_up = up_coord != last_coord and up_coord[1] > 0 and is_open_space(up_coord)  # and new_up_state != prior_moves
    can_go_down = down_coord != last_coord and is_open_space(down_coord) # and new_down_state != prior_moves
    can_go_left = left_coord != last_coord and left_coord[0] > 0 and is_open_space(left_coord) # and new_left_state != prior_moves
    can_go_right = right_coord != last_coord and is_open_space(right_coord) # and new_right_state != prior_moves

    # print 'up, down, left, right', new_coord, can_go_up, can_go_down, can_go_left, can_go_right

    # if can_go_up and up_coord == target_coord:
    #     return True
    # if can_go_down and down_coord == target_coord:
    #     return True
    # if can_go_left and left_coord == target_coord:
    #     return True
    # if can_go_right and right_coord == target_coord:
    #     return True

    found = False

    if can_go_up:
        # print 'going up from %s to %s' % (new_coord, up_coord)
        found = make_move(up_coord, new_coord, prior_moves, moves + 1, depth)
    if found:
        return True
    if can_go_down:
        # print 'going down from %s to %s' % (new_coord, down_coord)
        found = make_move(down_coord, new_coord, prior_moves, moves + 1, depth)
    if found:
        return True
    if can_go_left:
        # print 'going left from %s to %s' % (new_coord, left_coord)
        found = make_move(left_coord, new_coord, prior_moves, moves + 1, depth)
    if found:
        return True
    if can_go_right:
        # print 'going right from %s to %s' % (new_coord, right_coord)
        found = make_move(right_coord, new_coord, prior_moves, moves + 1, depth)

    return found

visited = set()
# make_move((1, 1), (None, None), visited, 0, 1)

for x in range(1, 100):
    print 'trying depth', x
    make_move((1, 1), (None, None), visited, 0, x)
