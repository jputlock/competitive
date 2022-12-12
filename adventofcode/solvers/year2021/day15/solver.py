from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import sys
import heapq
import itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def least_risky_path(grid, mult):
    width = len(grid[0])
    height = len(grid)

    weights = {
        (x, y): ((grid[y % height][x % width] + (x // width) + (y // height)) % 9) + 1
        for x in range(mult * width)
        for y in range(mult * height)
    }

    graph = nx.DiGraph()
    for x, y in weights:
        for pos in [(x + dx, y + dy) for dx, dy in offsets]:
            if 0 <= pos[0] < mult * width and 0 <= pos[1] < mult * height:
                graph.add_edge((x, y), pos, weight=weights[pos])

    start = (0, 0)
    end = (mult * width - 1, mult * height - 1)
    path = nx.shortest_path(graph, start, end, weight="weight")

    return sum(weights[pos] for pos in path[1:])


def solve(input: str) -> Generator[any, None, None]:
    grid = [[int(x) - 1 for x in line] for line in input.split("\n")]

    for multiplier in [1, 5]:
        yield least_risky_path(grid, multiplier)
