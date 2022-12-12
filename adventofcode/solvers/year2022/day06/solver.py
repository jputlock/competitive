from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]
    line = lines[0]

    def get_num_scanned(line: str, offset: int):
        for i in range(len(line)):
            if len(set(line[i : i + offset])) == offset:
                return i + 4

    # Part 1
    yield get_num_scanned(line, 4)

    # Part 2
    yield get_num_scanned(line, 14)
