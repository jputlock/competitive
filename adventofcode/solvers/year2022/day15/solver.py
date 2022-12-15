from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    known = {}

    targety = 2_000_000

    sensors = []

    for line in lines:
        mymatch = re.search(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        sx, sy, cx, cy = [int(x) for x in mymatch.groups()]
        known[(sx, sy)] = "S"
        known[(cx, cy)] = "B"

        max_dist = abs(sx - cx) + abs(sy - cy)
        sensors.append((sx, sy, max_dist))

        dy = abs(targety - sy)
        for dx in range(-(max_dist - dy), max_dist - dy + 1):
            if known.get((sx + dx, targety), None) is None:
                known[sx + dx, targety] = "#"

    # minx = min(x for x, _ in known)
    # maxx = max(x for x, _ in known)
    # miny = min(y for _, y in known)
    # maxy = max(y for _, y in known)
    # # print(minx, maxx)
    # for y in range(miny, maxy + 1):
    #     for x in range(minx, maxx + 1):
    #         print(known.get((x, y), "."), end="")
    #     if y == 10:
    #         print("<--------", end="")
    #     print()

    # Part 1
    yield len([v for (_, y), v in known.items() if y == targety and v == "#"])

    locs = set()
    for (sx, sy, dist) in sensors:
        for xx in [-1, 1]:
            for yy in [-1, 1]:
                for dx in range(dist + 2):
                    dy = dist + 1 - dx
                    x = sx + dx * xx
                    y = sy + dy * yy
                    if not (0 < x < 4000000) or not (0 < y < 4000000):
                        return False
                    valid = True
                    for (cx, cy, cdist) in sensors:
                        if abs(cx - x) + abs(cy - y) <= cdist:
                            valid = False
                            break
                    if valid:
                        return 4000000 * x + y

        # for dx in range(-dist - 1, dist + 1 + 1):
        #     for dy in [-(max_dist + 1 - abs(dx)), max_dist + 1 - abs(dx)]:
        #         x, y = sx + dx, sy + dy
        #         if not (0 < x < 4000000) or not (0 < y < 4000000):
        #             continue
        #         if (x, y) in locs:
        #             continue
        #         locs.add((x, y))
