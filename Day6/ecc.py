#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input.txt')]

corrected_string = []

histograms = [{} for i in range(0, len(INPUTS[0]))]

for line in INPUTS:
    list_line = list(line)

    for index in range(0, len(list_line)):
        histogram = histograms[index]
        char = list_line[index]

        if char in histogram:
            histogram[char] = histogram[char] + 1
        else:
            histogram[char] = 1

code = ''

for histogram in histograms:
    found_char = None
    compare_val = 1000

    for key, value in histogram.items():
        if value < compare_val:
            compare_val = value
            found_char = key

    code += found_char

print code
