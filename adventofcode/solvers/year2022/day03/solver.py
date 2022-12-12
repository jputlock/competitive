from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def map_value(char: str):
    if char > "a":
        return ord(char) - 97 + 1
    else:
        return ord(char) - 65 + 27


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    splitlines = [[line[: len(line) // 2], line[len(line) // 2 :]] for line in lines]

    total = 0

    for [a, b] in splitlines:
        intersection = set(a).intersection(set(b))

        for val in intersection:
            total += map_value(val)

    # Part 1
    yield total

    total = 0
    for i in range(0, len(lines), 3):
        intersection = set.intersection(*map(set, lines[i : i + 3]))
        for val in intersection:
            total += map_value(val)

    yield total
