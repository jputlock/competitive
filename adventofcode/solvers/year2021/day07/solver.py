from typing import Generator
from collections import defaultdict as dd
import numpy as np
import re
import sys


dist1 = abs
dist2 = lambda x: abs((x * (x + 1)) // 2)


def solve(input: str) -> Generator[any, None, None]:
    nums = list(map(int, input.split(",")))

    # Part 1
    yield min(
        sum(dist1(num - median) for num in nums)
        for median in range(min(nums), max(nums) + 1)
    )

    # Part 2
    yield min(
        sum(dist2(num - median) for num in nums)
        for median in range(min(nums), max(nums) + 1)
    )
