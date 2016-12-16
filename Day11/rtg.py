#!/usr/bin/env python

import itertools
import pprint
import copy


INPUTS = [line.rstrip('\n') for line in open('input2.txt')]

move_count = 0


class ExperimentItem:
    element = None
    item_type = None

    def __init__(self, element):
        self.element = element

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '%s %s' % (self.element, self.item_type)

    def is_safe_to_be_on_a_floor_with_items(self, items):
        assert 'should be implemented by subclass'


class RTG(ExperimentItem):
    item_type = 'rtg'

    def is_safe_to_be_on_a_floor_with_items(self, items):
        safe = True
        will_have_matching_rtg = False

        for item in items:
            if item.item_type == 'microchip':
                if item.element == self.element:
                    will_have_matching_rtg = True
                else:
                    safe = False

        return will_have_matching_rtg or safe


class Microchip(ExperimentItem):
    item_type = 'microchip'

    def is_safe_to_be_on_a_floor_with_items(self, items):
        safe = True
        will_have_matching_rtg = False

        for item in items:
            if item.item_type == 'rtg':
                if item.element == self.element:
                    will_have_matching_rtg = True
                else:
                    safe = False

        return will_have_matching_rtg or safe


class Floor:
    items = []
    building = None
    level = 0

    def __init__(self, building, level):
        self.items = []
        self.building = building
        self.level = level

    @property
    def is_empty(self):
        return len(self.items) == 0

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        print item, self.items, item in self.items
        self.items.remove(item)


class Elevator:
    building = None
    floor = 0
    items = []
    moves = 0

    def __init__(self, building):
        self.floor = 0
        self.moves = 0
        self.building = building
        self.items = []

    @property
    def can_move(self):
        return len(self.items) > 0

    @property
    def is_full(self):
        return len(self.items) == 2

    def select_items_to_move(self, direction=1):
        items_on_floor = self.building.floors[self.floor].items
        items_on_next_floor = self.building.floors[self.floor + direction].items
        items_that_can_move = []

        for item in items_on_floor:
            potential_move = items_that_can_move + items_on_next_floor
            if item.is_safe_to_be_on_a_floor_with_items(potential_move):
                items_that_can_move.append(item)

        return items_that_can_move

    @property
    def possible_directions(self):
        directions = [1, -1]

        if self.floor == 0:
            directions.remove(-1)
        if self.floor == len(self.building.floors) - 1:
            directions.remove(1)

        return directions

    def possible_moves(self):
        possible_moves = {
            1: set(),
            -1: set()
        }

        items_on_floor = self.building.floors[self.floor].items

        for direction in self.possible_directions:
            items_on_next_floor = self.building.floors[
                self.floor + direction].items

            for grouping in itertools.combinations(items_on_floor, 2):
                potential_move = list(grouping) + items_on_next_floor
                safe = True
                for item in grouping:
                    if not item.is_safe_to_be_on_a_floor_with_items(potential_move):
                        safe = False
                if safe:
                    possible_moves[direction].add(grouping)

            for item in items_on_floor:
                potential_move = list(items_on_next_floor)
                potential_move.append(item)
                safe = True
                if not item.is_safe_to_be_on_a_floor_with_items(potential_move):
                    safe = False
                if safe:
                    # make sure we can leave other items behind if we only move
                    # this one item
                    left_behind = list(items_on_floor)
                    left_behind.remove(item)
                    for left_behind_item in left_behind:
                        other_items = list(left_behind)
                        other_items.remove(left_behind_item)
                        # print 'other_items', item, left_behind_item, other_items, left_behind
                        if not left_behind_item.is_safe_to_be_on_a_floor_with_items(other_items):
                            safe = False
                if safe:
                    possible_moves[direction].add((item,)) # tuple for consistency

        return possible_moves

    def move_items_in_direction(self, items, direction=1):
        new_floor = self.floor + direction
        self.moves += 1
        for item in items:
            self.building.floors[new_floor].add_item(item)
            self.building.floors[self.floor].remove_item(item)
        self.floor += direction


class Building:
    floor0 = floor1 = floor2 = floor3 = None
    floors = []
    elevator = None
    move_count = 0

    def __init__(self):
        self.reset()

    def __str__(self):
        building_str = ''
        for floor in reversed(building.floors):
            building_str += 'Floor %s: ' % floor.level
            for item in floor.items:
                building_str += str(item) + ', '
            if self.elevator.floor == floor.level - 1:
                building_str += '*'
            building_str += '\n'
        return building_str

    @property
    def all_items_are_on_top_floor(self):
        top_heavy = True
        for floor in [self.floor0, self.floor1, self.floor2]:
            if not floor.is_empty:
                top_heavy = False
        return top_heavy

    def reset(self):
        self.floor0 = Floor(building=self, level=1)
        self.floor0.items.append(Microchip('hydrogen'))
        self.floor0.items.append(Microchip('lithium'))

        self.floor1 = Floor(building=self, level=2)
        self.floor1.items.append(RTG('hydrogen'))

        self.floor2 = Floor(building=self, level=3)
        self.floor2.items.append(RTG('lithium'))

        self.floor3 = Floor(building=self, level=4)

        self.floors = [self.floor0, self.floor1, self.floor2, self.floor3]
        self.elevator = Elevator(building=self)

    def start(self):
        global move_count
        done = self.all_items_are_on_top_floor
        while not done or move_count < 50:
            possible_moves = self.elevator.possible_moves()
            for k, v in possible_moves.iteritems():
                if done:
                    break
                for move in v:
                    if done:
                        break
                    move_count += 1
                    self.elevator.move_items_in_direction(move, k)
                    new_building = copy.deepcopy(self)
                    print new_building
                    if new_building.all_items_are_on_top_floor:
                        done = True
                    else:
                        new_building.start()
                    # if self.all_items_are_on_top_floor:
                    #     done = True



building = Building()
print building
building.start()
# items_to_move = building.elevator.select_items_to_move()
# print "POSSIBLE MOVES"
# pprint.pprint(building.elevator.possible_moves())
# building.elevator.move_items_in_direction(items_to_move)
# print "NOW"
# print building
# new_building = copy.deepcopy(building)
# print "NEW BUILDING"
# print new_building
# print new_building.elevator.floor
# print "POSSIBLE MOVES"
# pprint.pprint(building.elevator.possible_moves())
# items_to_move = building.elevator.select_items_to_move()
# building.elevator.move_items_in_direction(items_to_move)
# print "NOW"
# print building
# print "POSSIBLE MOVES"
# a = building.elevator.possible_moves()
# pprint.pprint(a)
