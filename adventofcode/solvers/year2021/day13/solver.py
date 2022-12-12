from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools


def solve(input: str) -> Generator[any, None, None]:
    sections = [line for line in input.split("\n\n") if line]

    paper = dd(bool)

    for line in sections[0].split("\n"):
        x, y = [int(x) for x in line.split(",")]
        paper[(x, y)] = True

    instructions = []

    for line in sections[1].split("\n"):
        if not line:
            continue
        groups = re.match("fold along (\w)=(\d+)", line).groups()
        instructions.append((groups[0], int(groups[1])))

    for inst_num, instruction in enumerate(instructions):
        which_axis, axis = instruction
        new_paper = dd(bool)
        for (x, y) in paper:
            if which_axis == "x":
                if x < axis:
                    new_paper[(x, y)] = True
                else:
                    new_paper[(2 * axis - x, y)] = True
            elif which_axis == "y":
                if y < axis:
                    new_paper[(x, y)] = True
                else:
                    new_paper[(x, 2 * axis - y)] = True
        paper = new_paper

        # Part 1
        if inst_num == 0:
            yield len(paper)

    xs = set(x for x, _ in paper)
    ys = set(y for _, y in paper)

    grid = [[" " for _ in range(max(xs) + 1)] for _ in range(max(ys) + 1)]

    for (x, y) in paper:
        grid[y][x] = "#"

    print("\n".join("".join(ln) for ln in grid))
    yield "UCLZRAZU"
