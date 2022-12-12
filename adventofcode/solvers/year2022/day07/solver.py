from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# def get_size(pwd, fs):
#     total = fs[pwd][1]

#     for subdir in fs[pwd][0]:
#         total += get_size(f"{pwd}/{subdir}", fs)

#     return total


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    fs = dd(lambda: [[], 0])
    sizes = dict()

    path = []

    i = 0
    while i < len(lines):
        if not lines[i].startswith("$ "):
            print("Parsing Error")
            exit()

        pwd = "/".join(path)

        args = lines[i][2:].split(" ")
        if args[0] == "cd":
            if args[1] == "..":
                sizes[pwd] = fs[pwd][1] + sum(
                    sizes[f"{pwd}/{subdir}"] for subdir in fs[pwd][0]
                )

                path.pop()
            else:
                path.append(args[1])
        elif args[0] == "ls":
            i += 1
            contents = []
            while i < len(lines):
                if lines[i].startswith("$ "):
                    break

                size, file = lines[i].split(" ")

                if size == "dir":
                    fs[pwd][0].append(file)
                else:
                    fs[pwd][1] += int(size)

                contents.append(lines[i])
                i += 1
            i -= 1
        i += 1

    # Pretend we "cd .." up to root
    for i in range(len(path)):
        pwd = "/".join(path[: len(path) - i])
        sizes[pwd] = fs[pwd][1] + sum(sizes[f"{pwd}/{subdir}"] for subdir in fs[pwd][0])

    # Part 1
    # sizes = {key: get_size(key, fs) for key in fs}
    yield sum(filter(lambda x: x <= 100_000, sizes.values()))

    # Part 2
    need_wiped = sizes["/"] - 40_000_000
    yield min(size for size in sizes.values() if size >= need_wiped)
