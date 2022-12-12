from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

mapping = {"X": 1, "Y": 2, "Z": 3}

map2 = {"A": 1, "B": 2, "C": 3}


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip().split(" ") for line in input.split("\n") if line]

    myscore = 0

    for [a, b] in lines:
        myscore += mapping[b]

        if b == "X":
            if a == "A":
                myscore += 3
            elif a == "B":
                myscore += 0
            elif a == "C":
                myscore += 6
        elif b == "Y":
            if a == "A":
                myscore += 6
            elif a == "B":
                myscore += 3
            elif a == "C":
                myscore += 0
        elif b == "Z":
            if a == "A":
                myscore += 0
            elif a == "B":
                myscore += 6
            elif a == "C":
                myscore += 3

    # Part 1
    yield myscore

    myscore = 0
    for [a, b] in lines:
        if b == "X":
            # lose
            myscore += 0 + (map2[a] + 1) % 3 + 1
        elif b == "Y":
            # draw
            myscore += 3 + map2[a]
        elif b == "Z":
            # win
            myscore += 6 + map2[a] % 3 + 1
    yield myscore
