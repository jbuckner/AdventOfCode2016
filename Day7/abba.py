#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input.txt')]

abbas = []

def has_abba(string):
    abba_found = False
    list_string = list(string)

    for idx, val in enumerate(list_string):
        if idx + 3 > len(list_string) - 1:
            continue
        outside_matches = list_string[idx] == list_string[idx + 3]
        inside_matches = list_string[idx + 1] == list_string[idx + 2]
        inside_matches_outside = list_string[idx] == list_string[idx + 1]

        current_comparison = [list_string[idx], list_string[idx+1], list_string[idx+2], list_string[idx+3]]

        if outside_matches and inside_matches and not inside_matches_outside:
            abba_found = True
            continue
    return abba_found

for line in INPUTS:
    strings_to_test = []
    bracket_strings = []
    new_string = ''
    in_brackets = False
    abba_found = False
    abba_found_in_brackets = False

    for char in list(line):
        if char == '[':
            strings_to_test.append(new_string)
            new_string = ''
            in_brackets = True
            continue

        if char == ']':
            bracket_strings.append(new_string)
            new_string = ''
            in_brackets = False
            continue

        new_string += char

    strings_to_test.append(new_string)

    for string in strings_to_test:
        list_string = list(string)

        if has_abba(list_string):
            abba_found = True
            continue

    for string in bracket_strings:
        list_string = list(string)

        if has_abba(list_string):
            abba_found_in_brackets = True
            continue

    if abba_found and not abba_found_in_brackets:
        abbas.append(line)

print len(abbas)
