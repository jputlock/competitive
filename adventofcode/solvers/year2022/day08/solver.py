from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    nums = np.array([[int(x) for x in line] for line in lines])

    part1 = np.zeros_like(nums, bool)
    part2 = np.ones_like(nums, int)

    for rot in range(4):
        for x, y in np.ndindex(nums.shape):
            decreasing = [t < nums[x, y] for t in nums[x, y + 1 :]]

            part1[x, y] |= all(decreasing)

            dist = len(decreasing)
            try:
                dist = decreasing.index(False) + 1
            except:
                pass

            part2[x, y] *= dist

        nums, part1, part2 = map(np.rot90, [nums, part1, part2])

    # Part 1
    yield int(np.sum(part1))

    # Part 2
    yield int(np.max(part2))
