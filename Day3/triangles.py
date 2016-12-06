#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input.txt')]
ROWS = []
TRIANGLES = []

for line in INPUTS:
    edges = filter(None, line.split(' '))
    row = [int(x) for x in edges]
    ROWS.append(row)

transform_index = 0
row_count = len(ROWS)

while transform_index < row_count:
    for col in range(0, 3):
        triangle = []
        for row in range(transform_index, transform_index + 3):
            triangle.append(ROWS[row][col])
        TRIANGLES.append(triangle)
    transform_index = transform_index + 3

triangle_count = 0

for triangle in TRIANGLES:
    possible = True
    if triangle[0] + triangle[1] <= triangle[2]:
        possible = False
    if triangle[0] + triangle[2] <= triangle[1]:
        possible = False
    if triangle[1] + triangle[2] <= triangle[0]:
        possible = False
    if possible:
        triangle_count = triangle_count + 1

print triangle_count
