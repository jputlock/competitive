from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [
    (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx != dy or dx != 0
]


def solve(input: str) -> Generator[any, None, None]:

    lines = [line.strip() for line in input.split("\n") if line]

    curr = np.array([[int(x) for x in line] for line in lines])

    flashes = 0
    for step in range(1, 1000):
        curr += 1

        to_pop = [(y, x) for y, x in zip(*np.where(curr > 9))]
        popped = set()

        while len(to_pop) > 0:
            y, x = to_pop.pop()
            for dy, dx in offsets:
                newy, newx = y + dy, x + dx
                if 0 <= newy < curr.shape[0] and 0 <= newx < curr.shape[1]:
                    curr[newy, newx] += 1
                    if (
                        curr[newy, newx] > 9
                        and (newy, newx) not in popped
                        and (newy, newx) not in to_pop
                    ):
                        to_pop.append((newy, newx))
            popped.add((y, x))

        num_flash = np.count_nonzero(curr > 9)
        flashes += num_flash
        if num_flash == 100:
            print(curr)
            yield step
            return
        curr[np.where(curr > 9)] = 0

        if step == 100:
            yield flashes
