from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools


def solve(input: str) -> Generator[any, None, None]:
    lines = [list(line.strip()) for line in input.split("\n") if line]
    WIDTH = len(lines[0])
    HEIGHT = len(lines)

    elves = set(
        (x, y) for y in range(HEIGHT) for x in range(WIDTH) if lines[y][x] == "#"
    )

    def north(x, y):
        return list((x + dx, y - 1) for dx in range(-1, 2))

    def south(x, y):
        return list((x + dx, y + 1) for dx in range(-1, 2))

    def west(x, y):
        return list((x - 1, y + dy) for dy in range(-1, 2))

    def east(x, y):
        return list((x + 1, y + dy) for dy in range(-1, 2))

    def neighbors(x, y):
        return set(
            (x + dx, y + dy)
            for dy in range(-1, 2)
            for dx in range(-1, 2)
            if dx != 0 or dy != 0
        )

    round = 1
    while True:
        moved = False
        new_elves = dd(list)
        for (x, y) in elves:

            if len(neighbors(x, y) & elves) == 0:
                new_elves[(x, y)] += [(x, y)]
                continue

            # Idea: If any elf is not completely isolated then some elf can move.
            moved = True

            dirs = [
                north(x, y),
                south(x, y),
                west(x, y),
                east(x, y),
            ]

            newpos = (x, y)
            for i in range(round, round + 4):
                if len(elves & set(dirs[i % 4])) == 0:
                    newpos = dirs[i % 4][1]
                    break
            new_elves[newpos] += [(x, y)]

        elves = set()
        for new_pos, from_lst in new_elves.items():
            if len(from_lst) == 1:
                elves.add(new_pos)
            else:
                elves |= set(from_lst)

        minx = min(x for x, _ in elves)
        maxx = max(x for x, _ in elves)
        miny = min(y for _, y in elves)
        maxy = max(y for _, y in elves)

        if round == 9:
            # Part 1
            yield (maxy - miny + 1) * (maxx - minx + 1) - len(elves)

        if not moved:
            break

        round += 1

    yield round
