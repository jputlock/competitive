from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools


def solve(input: str) -> Generator[any, None, None]:
    template, text_rules = input.split("\n\n")
    template = [x for x in template]

    rules = dict()
    for line in text_rules.split("\n"):
        if not line:
            continue
        rule = re.match("(\w+) -> (\w+)", line)
        a, b = rule.groups()
        rules[a] = b

    current = dd(int)
    for a, b in zip(template[:-1], template[1:]):
        current[a + b] += 1

    for step in range(1, 40 + 1):
        new = dd(int)
        for key, val in current.items():
            rule = rules.get(key, None)
            if rule is None:
                continue

            key1 = key[0] + rule
            key2 = rule + key[1]
            new[key1] += val
            new[key2] += val
        current = new

        if step in [10, 40]:

            tmp = dd(int)
            for combo, val in current.items():
                tmp[combo[0]] += val
            tmp[template[-1]] += 1

            yield max(tmp.values()) - min(tmp.values())
