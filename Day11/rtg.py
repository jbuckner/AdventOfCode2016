#!/usr/bin/env python

import itertools
import pprint
import copy
import pdb

from datetime import datetime

INPUTS = [line.rstrip('\n') for line in open('input2.txt')]

move_count = 0
building_id = 0


class ExperimentItem:
    element = None
    item_type = None

    def __init__(self, element):
        self.element = element

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash('%s%s' % (self.element, self.item_type))

    def __eq__(self, other):
        # print self, other
        # print self.element == other.element, self.item_type == other.item_type
        return (self.element == other.element and
                self.item_type == other.item_type)

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

    # def __hash__(self):
    #     items_hash = [hash(item) for item in self.items]
    #     return hash('%s%s%s' % (self.level, len(self.items), items_hash))

    def __eq__(self, other):
        if self.level != other.level:
            return False
        if len(self.items) != len(other.items):
            return False
        for item in self.items:
            found = False
            for other_item in other.items:
                if item == other_item:
                    found = True
            if not found:
                return False
        # print 'equals', self, other
        return True

    @property
    def is_empty(self):
        return len(self.items) == 0

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        # print item, self.items, item in self.items
        self.items.remove(item)

    def get_item_of_type(self, item_type, element):
        for item in self.items:
            if item.item_type == item_type and item.element == element:
                return item
        return None


class Elevator:
    building = None
    floor = 0
    items = []
    moves = 0
    previous_moves = []

    def __init__(self, building):
        self.floor = 0
        self.moves = 0
        self.building = building
        self.items = []
        self.previous_moves = []

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
            -1: set(),
            1: set()
        }

        items_on_floor = self.building.floors[self.floor].items

        # print 'previous_moves', self.previous_moves

        for direction in self.possible_directions:
            possible_moves[direction] = set()

            items_on_next_floor = self.building.floors[
                self.floor + direction].items

            for grouping in itertools.combinations(items_on_floor, 2):
                potential_move = list(grouping) + items_on_next_floor
                safe = True
                for item in grouping:
                    if not item.is_safe_to_be_on_a_floor_with_items(potential_move):
                        safe = False
                # we don't want to replay the last move
                if safe:
                    # print 'last move grouping', self.last_move
                    for prev_move in self.previous_moves:
                        prev_move_items = prev_move['items']
                        if len(prev_move_items) < 2:
                            continue
                        # print 'last move single', self.last_move, direction, self.last_move['direction'] * -1, item, item == self.last_move['items']
                        # print id(self.last_move['items']), id(i?tem)
                        if (direction == prev_move['direction'] * -1):
                            # print 'prev move', grouping, prev_move
                            if ((grouping[0] == prev_move_items[0] or
                                 grouping[0] == prev_move_items[1]) and
                                (grouping[1] == prev_move_items[0] or
                                 grouping[1] == prev_move_items[1])):
                                safe = False
                if safe:
                    # print possible_moves, grouping, direction
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

                # item_entry = item  # tuple for consistency

                # we don't want to replay and previous moves
                if safe:
                    for prev_move in self.previous_moves:
                        # print item, prev_move['items'], item == prev_move['items']
                        if (direction == prev_move['direction'] * -1 and
                            [item] == prev_move['items']):
                            safe = False

                if safe:
                    possible_moves[direction].add((item,))

        return possible_moves

    def move_items_in_direction(self, items, direction=1):
        last_move = {
            'direction': direction,
            'items': items
        }
        self.previous_moves = [last_move]
        new_floor = self.floor + direction
        self.moves += 1
        for item in items:
            self.building.floors[new_floor].add_item(item)
            self.building.floors[self.floor].remove_item(item)
        self.floor += direction

    def get_item_of_type_from_floor(self, item_type, element):
        return self.building.floors[self.floor].get_item_of_type(
            item_type, element)


class Building:
    created_by = None
    name = None
    floor0 = floor1 = floor2 = floor3 = None
    floors = []
    elevator = None
    move_count = 0

    def __init__(self):
        # self.sample()
        self.real_data()

    def __eq__(self, other):
        if self.elevator.floor != other.elevator.floor:
            return False
        for floor in self.floors:
            matches = False
            for other_floor in other.floors:
                if floor == other_floor:
                    matches = True
            if not matches:
                return False
        return True

    def __str__(self):
        building_str = 'Building %s, created by: %s\n' % (self.name, self.created_by)
        for floor in reversed(self.floors):
            building_str += 'Floor %s: ' % floor.level
            for item in floor.items:
                building_str += str(item) + ', '
            if self.elevator.floor == floor.level - 1:
                building_str += '*'
            building_str += '\n'
        return building_str

    # handles names and IDs and such
    def make_a_copy(self):
        new_building = copy.deepcopy(self)
        new_building.created_by = self.name
        new_building.name += 1
        return new_building

    @property
    def all_items_are_on_top_floor(self):
        top_heavy = True
        for floor in [self.floor0, self.floor1, self.floor2]:
            if not floor.is_empty:
                top_heavy = False
        return top_heavy

    def sample(self):
        self.name = building_id

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

    def real_data(self):
        self.name = building_id

        self.floor0 = Floor(building=self, level=1)
        self.floor0.items.append(RTG('promethium'))
        self.floor0.items.append(Microchip('promethium'))

        self.floor1 = Floor(building=self, level=2)
        self.floor1.items.append(RTG('cobalt'))
        self.floor1.items.append(RTG('curium'))
        self.floor1.items.append(RTG('ruthenium'))
        self.floor1.items.append(RTG('plutonium'))

        self.floor2 = Floor(building=self, level=3)
        self.floor2.items.append(Microchip('cobalt'))
        self.floor2.items.append(Microchip('curium'))
        self.floor2.items.append(Microchip('ruthenium'))
        self.floor2.items.append(Microchip('plutonium'))

        self.floor3 = Floor(building=self, level=4)

        self.floors = [self.floor0, self.floor1, self.floor2, self.floor3]
        self.elevator = Elevator(building=self)

    def make_move(self, depth=1):
        if self.elevator.moves > depth:
            return False

        if self.all_items_are_on_top_floor:
            print 'SOLUTION FOUND, MOVES:', self.elevator.moves
            return self

        possible_moves = self.elevator.possible_moves()
        up_moves = possible_moves[1]
        down_moves = possible_moves[-1]

        if len(up_moves) == 0 and len(down_moves) == 0:
            return False

        for direction, moves in possible_moves.iteritems():
            for items in list(moves):
                new_building = self.make_a_copy()

                items_to_move = []
                for item in items:
                    item_to_move = new_building.elevator.get_item_of_type_from_floor(item.item_type, item.element)
                    if item_to_move:
                        items_to_move.append(item_to_move)
                new_building.elevator.move_items_in_direction(items_to_move, direction)

                # don't go back down this path
                if new_building in buildings_seen:
                    print 'path previously visited'
                    # print new_building
                    continue

                buildings_seen.append(new_building)

                if new_building.make_move(depth):
                    return new_building
                else:
                    continue


building = Building()
buildings_seen = []

for x in range(12, 100):
    buildings_seen = []
    buildings_seen.append(building)
    print '*************'
    print 'start time: %s, depth: %s' % (str(datetime.now()), x)
    print '*************'
    success = building.make_move(x)
    if success:
        print 'found at %s, depth: %s', str(datetime.now()), x
        print success
        break
