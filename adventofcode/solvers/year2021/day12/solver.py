from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools


def find_paths1(graph: nx.Graph, current: str, visited: set = set()):
    if current == "end":
        return 1
    if current.islower() and current in visited:
        return 0
    visited = visited | {current}

    num_paths = 0
    for neighbor in graph[current]:
        num_paths += find_paths1(graph, neighbor, visited)

    return num_paths


def find_paths2(graph: nx.Graph, current: str, visited: set = set(), smol=None):
    if current == "end":
        return 1
    if current == "start" and visited:
        return 0
    if current.islower() and current in visited:
        if smol is None:
            smol = current
        else:
            return 0
    visited = visited | {current}

    num_paths = 0
    for neighbor in graph[current]:
        num_paths += find_paths2(graph, neighbor, visited, smol)

    return num_paths


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    graph = nx.Graph()

    for line in lines:
        a, b = line.split("-")
        graph.add_edge(a, b)

    yield find_paths1(graph, "start")
    yield find_paths2(graph, "start")
