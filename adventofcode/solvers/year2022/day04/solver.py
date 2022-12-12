from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def contains(a, b):
    return a[0] <= b[0] and a[1] >= b[1]


def overlaps(a, b):
    return a[0] <= b[0] <= a[1]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    pairs = [
        [list(map(int, grp.split("-"))) for grp in line.split(",")] for line in lines
    ]

    total = 0
    for [a, b] in pairs:
        if contains(a, b) or contains(b, a):
            total += 1

    yield total

    count = 0

    for [a, b] in pairs:
        if overlaps(a, b) or overlaps(b, a):
            count += 1

    yield count
