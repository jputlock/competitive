from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools


def simulate(v_x: int, v_y: int, x_bounds, y_bounds):

    max_height = -math.inf

    x, y = 0, 0
    for _ in range(1000):
        x += v_x
        y += v_y

        max_height = max(max_height, y)
        if x_bounds[0] <= x <= x_bounds[1] and y_bounds[0] <= y <= y_bounds[1]:
            # return max_height
            return True
        if v_y < 0 and y < y_bounds[0]:
            return False
        if v_x > 0 and x > x_bounds[1]:
            return False
        if v_x == 0 and not (x_bounds[0] <= x <= x_bounds[1]):
            return False

        if v_x != 0:
            v_x = (v_x - 1) if v_x > 0 else (v_x + 1)
        v_y -= 1

    return False


def solve(input: str) -> Generator[any, None, None]:
    blah = re.match("target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", input)
    min_x, max_x, min_y, max_y = [int(x) for x in blah.groups()]

    num = 0

    for v_x in range(2000):
        for v_y in range(min_y, 1000):
            # max_height = max(
            #     max_height, simulate(v_x, v_y, (min_x, max_x), (min_y, max_y))
            # )
            num += int(simulate(v_x, v_y, (min_x, max_x), (min_y, max_y)))
    yield num

    # yield max_height
