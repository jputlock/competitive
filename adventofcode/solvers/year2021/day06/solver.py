from typing import Generator
from collections import defaultdict as dd
import numpy as np
import re


def solve(input: str) -> Generator[any, None, None]:
    # input = "3,4,3,1,2"
    nums = [int(x) for x in input.split(",")]

    counts = [nums.count(i) for i in range(9)]

    for day in range(256):
        num_born = counts.pop(0)

        counts[6] += num_born
        counts.append(num_born)

        if day == 80:
            yield sum(counts)

    yield sum(counts)
