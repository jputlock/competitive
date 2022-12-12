from typing import Generator
from collections import defaultdict as dd
from collections import deque
import numpy as np
import networkx as nx
import re, itertools


mapper = {"(": ")", "[": "]", "{": "}", "<": ">"}

score_lookup = {")": 1, "]": 2, "}": 3, ">": 4}


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    queue = []

    bad = dd(int)

    new_lines = []

    for line in lines:
        for x in line:
            if x in mapper.keys():
                queue.append(x)
            else:
                last = queue.pop()
                if x != mapper[last]:
                    bad[x] += 1
                    break
        else:
            new_lines.append(line)

    yield 3 * bad[")"] + 57 * bad["]"] + 1197 * bad["}"] + 25137 * bad[">"]

    scores = []
    for line in new_lines:
        score = 0
        queue = []
        for x in line:
            if x in mapper.keys():
                queue.append(x)
            else:
                last = queue.pop()

        for x in reversed(queue):
            score *= 5
            score += score_lookup[mapper[x]]

        scores.append(score)

    yield np.median(scores)
