#!/usr/bin/env python

import sys
import time
INPUTS = [line.rstrip('\n') for line in open('input.txt')]


class LCD:
    width = 0
    height = 0
    matrix = []

    def __init__(self, width, height):
        self.width = width
        self.height = height

        for y in range(0, self.height):
            self.matrix.append(['.' for x in range(0, self.width)])

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        lcd_string = ''
        for row in self.matrix:
            lcd_string += ''.join(row)
            lcd_string += '\n'
        return lcd_string

    def draw_rect(self, width, height):
        for y in range(0, height):
            for x in range(0, width):
                self.matrix[y][x] = '#'

    def rotate_column(self, col_x, count):
        pass

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

class Parser:
    pass

lcd = LCD(50, 10)
lcd.draw_rect(10, 5)

print lcd

for x in range(0, 10):
    lcd.rotate_row(0, 3)
    print lcd
    time.sleep(.1)
