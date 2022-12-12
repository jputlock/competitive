from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def update(register, cycle, score):
    if cycle in [20, 60, 100, 140, 180, 220]:
        score[0] += register * cycle


def draw(register, cycle, output):
    if abs(register - ((cycle - 1) % 40)) <= 1:
        output.append("#")
    else:
        output.append(".")


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    register = 1
    cycle = 1

    score = [0]
    output = []

    for line in lines:
        # print(cycle, register)
        update(register, cycle, score)
        draw(register, cycle, output)
        if line == "noop":
            pass
        else:
            inst, val = line.split(" ")
            val = int(val)
            cycle += 1
            update(register, cycle, score)
            draw(register, cycle, output)
            register += val
        cycle += 1

    # Part 1
    yield score[0]

    # Part 2
    yield "\n".join("".join(output[40 * i : 40 * (i + 1)]) for i in range(6))
