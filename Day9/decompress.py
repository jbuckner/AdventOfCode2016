#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input.txt')]


for line in INPUTS:
    list_line = list(line)
    line_length = len(list_line)

    new_string = []
    in_marker = False
    parse_complete = False
    index = 0

    while index < line_length:
        val = list_line[index]

        if val == '(':
            closing_marker_index = None

            for i in range(index, line_length):
                if list_line[i] == ')':
                    closing_marker_index = i
                    break
            marker = list_line[index + 1:closing_marker_index]
            capture_size, repetitions = ''.join(marker).split('x')
            capture_size = int(capture_size)
            repetitions = int(repetitions)

            index = closing_marker_index + capture_size + 1

            capture_group_start_index = closing_marker_index + 1
            capture_group_end_index = capture_group_start_index + capture_size

            if capture_group_start_index > line_length:
                capture_group_start_index = line_length
            if capture_group_end_index > line_length:
                capture_group_end_index = line_length

            captured_group = list_line[capture_group_start_index:capture_group_end_index]

            for x in range(0, repetitions):
                new_string += captured_group
        else:
            new_string += val
            index += 1

    decompressed = ''.join(new_string)
    print decompressed
    print 'length', len(decompressed)
