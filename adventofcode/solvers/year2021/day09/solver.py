from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re
import math

offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    depths = {
        (x, y): int(depth)
        for y, line in enumerate(lines)
        for x, depth in enumerate(line)
    }

    mins = []
    graph = nx.Graph()

    for (x, y), depth in depths.items():
        if all(depth < depths.get((x + dx, y + dy), math.inf) for (dx, dy) in offsets):
            mins.append(depth)

        if depth == 9:
            continue

        for dx, dy in offsets:
            newx, newx = x + dx, y + dy
            if depths.get((newx, newx), 9) != 9:
                graph.add_edge((x, y), (newx, newx))

    yield sum(mins) + len(mins)

    # Part 2
    basins = sorted(len(cc) for cc in nx.connected_components(graph))
    yield math.prod(basins[-3:])
