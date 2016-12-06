#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input.txt')]
TRIANGLES = []

for candidate in INPUTS:
    edges = filter(None, candidate.split(' '))
    triangle = [int(x) for x in edges]
    TRIANGLES.append(triangle)

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
