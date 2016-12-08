#!/usr/bin/env python

import re

INPUTS = [line.rstrip('\n') for line in open('input.txt')]


def make_histogram(string):
    histogram = {}
    for letter in string:
        if letter == '-':
            continue
        if letter in histogram:
            histogram[letter] = histogram[letter] + 1
        else:
            histogram[letter] = 1
    return histogram

def make_frequency_histogram(histogram):
    frequency_histogram = {}
    for key, value in histogram.iteritems():
        if value in frequency_histogram:
            frequency_histogram[value].append(key)
        else:
            frequency_histogram[value] = [key]
        frequency_histogram[value] = sorted(frequency_histogram[value])
    return frequency_histogram

def make_sorted_list_from_histogram(histogram):
    values = [value for key, value in histogram.iteritems()]
    return sorted(set(values), reverse=True)

def decrypt_name(encrypted_name, sector_id):
    shift = sector_id % 26
    decrypted_name = ''
    for char in encrypted_name:
        if char == '-':
            decrypted_name += ' '
            continue
        new_ascii = ord(char) + shift
        if new_ascii > 122:
            new_ascii = new_ascii - 26
        decrypted_name += chr(new_ascii)
    return decrypted_name

encrypted_names = []
sector_ids = []

for line in INPUTS:
    is_valid = True
    encrypted_name, sector_hash = line.rsplit('-', 1)
    matches = re.search(r'(\d+?)\[(\w*?)\].*', sector_hash)
    sector = int(matches.group(1))
    checksum = matches.group(2)
    histogram = make_histogram(encrypted_name)
    frequency_histogram = make_frequency_histogram(histogram)
    sorted_frequencies = make_sorted_list_from_histogram(histogram)

    position = None
    previous_char = None
    for index in range(0, len(checksum) - 1):
        char_check = checksum[index]
        char_frequency = None

        # print "char_check", char_check, index, char_frequency
        # is this character of the checksum in the encrypted name at all
        # if so, get its frequency
        if char_check in histogram:
            char_frequency = histogram[char_check]
        else:
            is_valid = False
            break

        # if this is the first character of the checksum, it should have the
        # most frequency (element 0 in sorted_frequencies)
        # otherwise, if a previous character's frequency is less than our
        # own, then it's also invalid
        if previous_char is None:
            if char_frequency != sorted_frequencies[0]:
                is_valid = False
                break
        else:
            if histogram[previous_char] < char_frequency:
                is_valid = False
                break

        # chars_with_frequency is sorted so it always has to be the first
        # because we pop the first off if it's found
        chars_with_frequency = frequency_histogram[char_frequency]
        if len(chars_with_frequency) > 0 and char_check == chars_with_frequency[0]:
            chars_with_frequency.pop(0)
        else:
            is_valid = False
            break

        previous_char = char_check

    if is_valid:
        encrypted_names.append(encrypted_name)
        sector_ids.append(sector)

print sum(sector_ids)

for index in range(0, len(encrypted_names) - 1):
    encrypted_name = encrypted_names[index]
    sector_id = sector_ids[index]
    decrypted_name = decrypt_name(encrypted_name, sector_id)
    print encrypted_name, sector_id, decrypted_name
