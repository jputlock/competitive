from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def sgn(x):
    return (1, -1)[x < 0]


def solve(input: str) -> Generator[any, None, None]:
    #     input = """R 5
    # U 8
    # L 8
    # D 3
    # R 17
    # D 10
    # L 25
    # U 20"""

    lines = [line.strip() for line in input.split("\n") if line]

    visited2 = dd(int)
    visited10 = dd(int)
    visited2[(0, 0)] = 1
    visited10[(0, 0)] = 1

    length = 10

    rope = [[0, 0] for _ in range(length)]

    for line_num, line in enumerate(lines):
        direction, amount = line.split(" ")
        amount = int(amount)

        # 0 = x, 1 = y
        axis = 0
        sign = 1

        if direction in ["L", "D"]:
            sign = -1
        if direction in ["U", "D"]:
            axis = 1

        for _ in range(amount):
            rope[0][axis] += sign
            for i in range(1, length):
                dx = rope[i][0] - rope[i - 1][0]
                dy = rope[i][1] - rope[i - 1][1]
                if dx == 0 or dy == 0:
                    if abs(dx) > 1:
                        rope[i][0] -= sgn(dx)
                    if abs(dy) > 1:
                        rope[i][1] -= sgn(dy)
                elif abs(dx) != 1 or abs(dy) != 1:
                    rope[i][0] -= sgn(dx)
                    rope[i][1] -= sgn(dy)

            visited2[tuple(rope[1])] += 1
            visited10[tuple(rope[9])] += 1

    yield len(visited2)
    yield len(visited10)
