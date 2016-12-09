#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input.txt')]

abbas = []
abas = []

def has_abba(string):
    abba_found = False
    list_string = list(string)

    for idx, val in enumerate(list_string):
        if idx + 3 > len(list_string) - 1:
            break
        outside_matches = list_string[idx] == list_string[idx + 3]
        inside_matches = list_string[idx + 1] == list_string[idx + 2]
        inside_matches_outside = list_string[idx] == list_string[idx + 1]

        current_comparison = [list_string[idx], list_string[idx+1], list_string[idx+2], list_string[idx+3]]

        if outside_matches and inside_matches and not inside_matches_outside:
            abba_found = True
            continue
    return abba_found

def has_matching_aba(string, aba):
    aba_found = False
    list_aba = list(aba)
    list_string = list(string)
    aba_to_find_list = [list_aba[1], list_aba[0], list_aba[1]]
    aba_to_find = ''.join(aba_to_find_list)
    if string.find(aba_to_find) > -1:
        return True
    return False

for line in INPUTS:
    strings_to_test = []
    bracket_strings = []
    new_string = ''
    in_brackets = False
    abba_found = False
    abba_found_in_brackets = False
    aba_found = False

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

        if aba_found:
            break

        for idx, val in enumerate(list_string):
            if aba_found:
                break

            if idx + 2 > len(list_string) - 1:
                break
            outside_matches = list_string[idx] == list_string[idx + 2]
            inside_matches_outside = list_string[idx] == list_string[idx + 1]
            current_comparison = ''.join([list_string[idx], list_string[idx+1], list_string[idx+2]])

            # print current_comparison, outside_matches, inside_matches_outside

            if outside_matches and not inside_matches_outside:
                for bracket_string in bracket_strings:
                    if has_matching_aba(bracket_string, current_comparison):
                        abas.append(line)
                        aba_found = True
                        print 'aba found', current_comparison, bracket_string
                        break

    for string in bracket_strings:
        list_string = list(string)

        if has_abba(list_string):
            abba_found_in_brackets = True

    if abba_found and not abba_found_in_brackets:
        abbas.append(line)

print len(abbas)
print len(abas)
