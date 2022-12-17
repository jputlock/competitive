from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def get_rock(t: int, y: int):
    if t == 0:
        return set([(2, y), (3, y), (4, y), (5, y)])
    elif t == 1:
        return set([(3, y + 2), (2, y + 1), (3, y + 1), (4, y + 1), (3, y)])
    elif t == 2:
        return set([(2, y), (3, y), (4, y), (4, y + 1), (4, y + 2)])
    elif t == 3:
        return set([(2, y), (2, y + 1), (2, y + 2), (2, y + 3)])
    elif t == 4:
        return set([(2, y + 1), (2, y), (3, y + 1), (3, y)])


def xmove(rock: set, dx: int):
    if dx == 1 and any(x == 6 for x, _ in rock):
        return rock
    elif dx == -1 and any(x == 0 for x, _ in rock):
        return rock
    return set((x + dx, y) for x, y in rock)


def ymove(rock: set, dy: int):
    return set((x, y + dy) for x, y in rock)


def solve(input: str) -> Generator[any, None, None]:
    gusts = [1 if x == ">" else -1 for x in input.strip()]

    highest_rock = 0
    turn = 0
    seen = {}

    NUM_ROCKS = 1_000_000_000_000

    extra = 0
    board = set((x, 0) for x in range(7))

    rock_num = 0
    while rock_num < NUM_ROCKS:
        this_rock = get_rock(rock_num % 5, highest_rock + 4)

        while True:
            this_gust = gusts[turn]
            # Perform a gust only if it doesnt go into other rocks
            new_rock = xmove(this_rock, this_gust)
            if not (new_rock & board):
                this_rock = new_rock
            turn = (turn + 1) % len(gusts)

            # Now go downwards
            new_rock = ymove(this_rock, -1)
            if not (new_rock & board):
                # No collision, continue
                this_rock = new_rock
            else:
                # We collided with previous rocks after moving

                # Add the rock (before moving) to the board
                board |= this_rock
                highest_rock = max(highest_rock, *[y for _, y in this_rock])

                topography = tuple(
                    highest_rock - max(y for x, y in board if x == i) for i in range(7)
                )
                # print(topography)

                id = (rock_num % 5, turn, topography)
                # Check for 2022 to ensure part 1 still prints
                if id in seen and rock_num >= 2022:
                    (old_rock_num, old_highest) = seen[id]
                    dy = highest_rock - old_highest
                    dr = rock_num - old_rock_num
                    num_cycles = (NUM_ROCKS - rock_num) // dr

                    extra += num_cycles * dy
                    rock_num += num_cycles * dr

                seen[id] = (rock_num, highest_rock)

                break
        rock_num += 1

        # Part 1
        if rock_num == 2022:
            yield highest_rock

    # Part 2
    yield highest_rock + extra
