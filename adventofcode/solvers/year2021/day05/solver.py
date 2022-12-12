from typing import Generator
import regex
from collections import defaultdict as dd

import numpy as np


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    board = dd(int)
    count = 0

    for line in lines:
        matched = regex.match(r"(\d+),(\d+) -> (\d+),(\d+)", line)
        x1, y1, x2, y2 = [int(x) for x in matched.groups()]

        # H / V lines
        if x1 == x2 or y1 == y2:
            minx = min(x1, x2)
            maxx = max(x1, x2)

            miny = min(y1, y2)
            maxy = max(y1, y2)

            for x in range(minx, maxx + 1):
                for y in range(miny, maxy + 1):
                    board[(x, y)] += 1
                    if board[(x, y)] == 2:
                        count += 1

        if np.abs(x2 - x1) == np.abs(y2 - y1):
            xstep = np.sign(x2 - x1)
            ystep = np.sign(y2 - y1)

            for x, y in zip(range(x1, x2 + xstep, xstep), range(y1, y2 + ystep, ystep)):
                board[(x, y)] += 1
                if board[(x, y)] == 2:
                    count += 1
    yield count
