#!/usr/bin/env python

import hashlib

INPUTS = [line.rstrip('\n') for line in open('input.txt')]


def decompress(string_as_list):
    string = ''.join(string_as_list)
    file_name = string
    file_path = 'tmp/%s.part' % hashlib.md5(file_name).hexdigest()
    # delete the old file
    with open(file_path, 'w'):
        pass
    with open(file_path, 'a') as new_file:
        index = 0
        line_length = len(string_as_list)

        while index < line_length:
            val = string_as_list[index]

            if val == '(':
                closing_marker_index = None

                for i in range(index, line_length):
                    if string_as_list[i] == ')':
                        closing_marker_index = i
                        break
                marker = string_as_list[index + 1:closing_marker_index]
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

                captured_group = string_as_list[capture_group_start_index:capture_group_end_index]

                decompressed_group_file_path = decompress(captured_group)

                with open(decompressed_group_file_path, 'r') as decompressed_part_file:
                    for line in decompressed_part_file:
                        for x in range(0, repetitions):
                            new_file.write(line)
            else:
                new_file.write(val)
                index += 1

        return file_path

for line in INPUTS:
    list_line = list(line)
    decompressed_file_path = decompress(list_line)

    length = 0

    with open(decompressed_file_path, 'r') as in_file:
        for line in in_file:
            length += len(line)

    print 'size in bytes:', length
