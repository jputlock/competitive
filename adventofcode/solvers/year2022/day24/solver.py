from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def add_and_wrap(a: tuple, b: tuple):
    return tuple((x + y) % m for x, y, m in zip(a, b, (WIDTH, HEIGHT)))


def neighborhood(point: tuple):
    (x, y) = point
    neighbors = set([(x, y)])
    if x - 1 >= 0 and 0 <= y < HEIGHT:
        neighbors.add((x - 1, y))
    if x + 1 < WIDTH and 0 <= y < HEIGHT:
        neighbors.add((x + 1, y))
    if y - 1 >= 0:
        neighbors.add((x, y - 1))
    if y + 1 < HEIGHT:
        neighbors.add((x, y + 1))
    return neighbors


def simulate(start, end, blizzards):
    prev_reachable = set([start])

    elapsed = 0
    live = True
    while live:
        # Find places to move
        reachable = set()
        for point in prev_reachable:
            for new_point in neighborhood(point) - blizzards.keys():
                reachable.add(new_point)
            if point in neighborhood(end):
                live = False
                break

        # Update blizzards
        new_blizzards = dd(list)
        for location, directions in blizzards.items():
            for direction in directions:
                new_location = add_and_wrap(location, direction)
                new_blizzards[new_location].append(direction)

        blizzards = new_blizzards
        prev_reachable = reachable
        elapsed += 1

    return elapsed, blizzards


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip()[1:-1] for line in input.split("\n")[1:-1] if line]

    global HEIGHT
    global WIDTH
    HEIGHT = len(lines)
    WIDTH = len(lines[0])

    # Start node
    S = (0, -1)
    # End node
    E = (WIDTH - 1, HEIGHT)

    blizzards = dd(list)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "<":
                blizzards[(x, y)].append((-1, 0))
            elif c == ">":
                blizzards[(x, y)].append((1, 0))
            elif c == "^":
                blizzards[(x, y)].append((0, -1))
            elif c == "v":
                blizzards[(x, y)].append((0, 1))

    m1, blizzards = simulate(S, E, blizzards)
    yield m1 - 1
    m2, blizzards = simulate(E, S, blizzards)
    m3, blizzards = simulate(S, E, blizzards)

    # Part 1
    yield m1 + m2 + m3 - 1
