from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    lowest = 0
    land = {}
    for line in lines:
        locations = line.split(" -> ")
        prevx, prevy = [int(z) for z in locations[0].split(",")]
        for location in locations[1:]:
            lowest = max(lowest, prevy)
            newx, newy = [int(z) for z in location.split(",")]

            for x in range(min(prevx, newx), max(prevx, newx) + 1):
                land[(x, prevy)] = "#"

            for y in range(min(prevy, newy), max(prevy, newy) + 1):
                land[(prevx, y)] = "#"

            prevx, prevy = newx, newy

    def my_solve(is_part2: bool, land: dict):
        live = True
        while live:
            x, y = 500, 0

            if land.get((x, y)) == "o":
                break

            while True:
                if not is_part2 and y >= lowest:
                    live = False
                    break
                if is_part2 and y == lowest + 1:
                    land[(x, y)] = "o"
                    break
                if land.get((x, y + 1), None) is None:
                    y += 1
                    continue
                elif land.get((x - 1, y + 1), None) is None:
                    x -= 1
                    y += 1
                    continue
                elif land.get((x + 1, y + 1), None) is None:
                    x += 1
                    y += 1
                    continue
                else:
                    land[(x, y)] = "o"
                    break
        return len(list(filter(lambda x: x == "o", land.values())))

    for is_part2 in [False, True]:
        yield my_solve(is_part2, land)
