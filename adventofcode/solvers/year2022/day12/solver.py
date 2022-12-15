from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools, sys

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    heights = dict()

    graph = nx.DiGraph()

    start = None
    starts = []
    end = None

    for y, line in enumerate(lines):
        for x, height in enumerate(line):
            graph.add_node((x, y))
            if height == "S":
                heights[(x, y)] = ord("a")
                start = (x, y)
                starts.append((x, y))
            elif height == "E":
                heights[(x, y)] = ord("z")
                end = (x, y)
            elif height == "a":
                heights[(x, y)] = ord(height)
                starts.append((x, y))
            else:
                heights[(x, y)] = ord(height)

    for y, line in enumerate(lines):
        for x, _ in enumerate(line):
            for dx, dy in offsets:
                if 0 <= x + dx < len(line) and 0 <= y + dy < len(lines):
                    if heights[(x + dx, y + dy)] - heights[(x, y)] <= 1:
                        graph.add_edge((x, y), (x + dx, y + dy))

    # Part 1
    yield len(nx.shortest_path(graph, start, end)) - 1

    # Part 2
    dist = sys.maxsize
    for s in starts:
        try:
            dist = min(dist, len(nx.shortest_path(graph, s, end)) - 1)
        except:
            pass

    yield dist
