from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

values = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}


def invert(x: int):
    if x == 0:
        return []
    elif x % 5 == 0:
        return invert(x // 5) + ["0"]
    elif x % 5 == 1:
        return invert(x // 5) + ["1"]
    elif x % 5 == 2:
        return invert(x // 5) + ["2"]
    elif x % 5 == 3:
        return invert((x + 2) // 5) + ["="]
    elif x % 5 == 4:
        return invert((x + 1) // 5) + ["-"]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    total = 0
    for line in lines:
        this_num = 0
        for c in line:
            this_num = 5 * this_num + values[c]

        total += this_num

    # Part 1
    yield "".join(invert(total))
