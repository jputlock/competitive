from typing import Generator


def solve(input: str) -> Generator[any, None, None]:
    nums = [int(line.strip()) for line in input.split()]

    # Part 1
    yield sum(
        a > b
        for a, b in zip(nums[1:], nums)
    )

    # Part 2
    windows = [sum(nums[i:i+3]) for i in range(len(nums) - 2)]
    yield sum(
        a > b
        for a, b in zip(windows[1:], windows)
    )