from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def compare(x, y):
    if type(x) is int and type(y) is int:
        if x == y:
            return None
        return x < y
    if type(x) is list and type(y) is list:
        for x1, y1 in zip(x, y):
            result = compare(x1, y1)
            if result is not None:
                return result
        if len(x) == len(y):
            return None
        return len(x) < len(y)
    # one is a list, one is an int
    x = [x] if type(x) is int else x
    y = [y] if type(y) is int else y

    return compare(x, y)


def solve(input: str) -> Generator[any, None, None]:
    pairs = input.split("\n\n")

    all_elements = []

    total = 0
    for index, pair in enumerate(pairs, 1):
        ele1, ele2 = [eval(x) for x in pair.split("\n")]
        result = compare(ele1, ele2)
        if result in [True, None]:
            total += index

        all_elements += [ele1, ele2]

    before_2 = 0
    before_6 = 0
    for element in all_elements:
        if compare(element, [[2]]) is True:
            before_2 += 1
            before_6 += 1
        elif compare(element, [[6]]) is True:
            before_6 += 1

    # Part 1
    yield total
    # Part 2
    yield (before_2 + 1) * (before_6 + 2)
