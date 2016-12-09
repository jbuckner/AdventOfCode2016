#!/usr/bin/env python

import time
INPUTS = [line.rstrip('\n') for line in open('input.txt')]


class LCD:
    unlit_pixel = ' '
    lit_pixel = '#'
    width = 0
    height = 0
    matrix = []

    def __init__(self, width, height):
        self.width = width
        self.height = height

        for y in range(0, self.height):
            self.matrix.append([self.unlit_pixel for x in range(0, self.width)])

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        lcd_string = ''
        for row in self.matrix:
            lcd_string += ''.join(row)
            lcd_string += '\n'
        return lcd_string

    @property
    def lit_pixel_count(self):
        count = 0
        for row in self.matrix:
            for col in row:
                if col != self.unlit_pixel:
                    count += 1
        return count

    def draw_rect(self, width, height):
        for y in range(0, height):
            for x in range(0, width):
                self.matrix[y][x] = self.lit_pixel

    def rotate_column(self, col_x, count):
        top = []
        bottom = []

        if count < 0:
            split = abs(count)
        else:
            split = self.height - abs(count)

        for y in range(0, self.height):
            char = self.matrix[y][col_x]

            if y < split:
                top.append(char)
            else:
                bottom.append(char)

        new_column = bottom + top

        for y in range(0, self.height):
            self.matrix[y][col_x] = new_column[y]

    def rotate_row(self, row_y, count):
        row = self.matrix[row_y]

        if count > 0:
            split = self.width - abs(count)
            left = row[split:self.width]
            right = row[0:split]
        else:
            split = abs(count)
            right = row[0:split]
            left = row[split:self.width]

        row[0:count] = left
        row[count:self.width] = right

lcd = LCD(50, 6)
print lcd

for line in INPUTS:
    parsed_line = line.split(' ')
    command = parsed_line[0]

    if command == 'rect':
        width, height = parsed_line[1].split('x')
        lcd.draw_rect(int(width), int(height))
    if command == 'rotate':
        coordinate = int(parsed_line[2].split('=')[1])  # x=1, it returns the 1
        distance = int(parsed_line[4])
        direction = parsed_line[1]

        if direction == 'row':
            lcd.rotate_row(coordinate, distance)
        if direction == 'column':
            lcd.rotate_column(coordinate, distance)

    print lcd
    time.sleep(.1)

print lcd.lit_pixel_count
