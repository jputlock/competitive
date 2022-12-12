from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(input: str) -> Generator[any, None, None]:
    # lines = [line.strip() for line in input.split("\n") if line]

    parta, partb = input.split("\n\n")

    stacks = [[] for _ in range(0, len(parta.split("\n")[0]), 4)]

    for line in parta.split("\n")[:-1]:
        for i, j in enumerate(range(1, len(line), 4)):
            if line[j] != " ":
                stacks[i].insert(0, line[j])

    for instruction in partb.split("\n"):
        mymatch = re.match(r"move (\d+) from (\d+) to (\d+)", instruction)

        count = int(mymatch.group(1))
        src = int(mymatch.group(2)) - 1
        dest = int(mymatch.group(3)) - 1

        # Part 1
        # for x in range(count):
        #     stacks[dest].append(stacks[src].pop())

        # Part 2
        stacks[dest] += stacks[src][-count:]
        stacks[src] = stacks[src][:-count]

    yield "".join(stack[-1] for stack in stacks)
