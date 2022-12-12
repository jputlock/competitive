from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(input: str) -> Generator[any, None, None]:

    rounds = 10_000

    monkeys = []

    monkey_groups = input.split("\n\n")
    for i, monkey_lines in enumerate(monkey_groups):
        lines = monkey_lines.split("\n")

        mdict = dict()

        mdict["items"] = list(map(int, lines[1][lines[1].index(":") + 1 :].split(", ")))
        mdict["op"] = lines[2][lines[2].index("new = ") + 6 :]
        mdict["mod"] = int(re.search(r"divisible by (\d+)", lines[3]).group(1))
        mdict[True] = int(re.search(r"monkey (\d+)", lines[4]).group(1))
        mdict[False] = int(re.search(r"monkey (\d+)", lines[5]).group(1))

        monkeys.append(mdict)

    inspected = dd(int)

    prod = 1
    for monkey in monkeys:
        prod *= monkey["mod"]

    for _ in range(rounds):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            for item in monkey["items"]:
                item = (lambda old: eval(monkey["op"]))(item)
                # item //= 3
                monkeys[monkey[item % monkey["mod"] == 0]]["items"].append(item % prod)

            inspected[i] += len(monkey["items"])
            monkey["items"] = []

    most = sorted(inspected.values())

    yield 0
    yield most[-1] * most[-2]
