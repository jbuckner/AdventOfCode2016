#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input.txt')]

registers = {
    'a': 0,
    'b': 0,
    'c': 1,
    'd': 0
}

index = 0

while index < len(INPUTS):
    line = INPUTS[index]
    command = line.split(' ')

    increment = 1

    # print line

    if command[0] == 'cpy':
        val = command[1]
        number_to_insert = None
        if val in ['a', 'b', 'c', 'd']:
            number_to_insert = registers[val]
        else:
            number_to_insert = int(val)

        register = command[2]
        registers[register] = number_to_insert
    if command[0] == 'inc':
        register = command[1]
        registers[register] += 1
    if command[0] == 'dec':
        register = command[1]
        registers[register] -= 1
    if command[0] == 'jnz':
        val = command[1]
        distance = int(command[2])
        number_to_check = None

        if val in ['a', 'b', 'c', 'd']:
            number_to_check = registers[val]
        else:
            number_to_check = int(val)

        if number_to_check != 0:
            increment = distance

    index += increment
    # print line
    # print index

print registers
