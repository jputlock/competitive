from typing import Generator, Tuple
from collections import defaultdict as dd
from collections import namedtuple
from functools import reduce
import numpy as np
import networkx as nx
import re, math, itertools

Explosion = namedtuple("Explosion", ["left", "right", "value"])


def unwrap(number):
    if isinstance(number, Explosion):
        return number.value
    return number


def snailfish_add(lhs, rhs):
    result = [lhs, rhs]

    changed = True
    while changed:
        changed, result = explode(result)
        result = unwrap(result)
        if changed:
            # Want to explode everything before splitting
            continue

        changed, result = split(result)
        result = unwrap(result)

    return result


def add_to_leftmost(number, value):
    if value is None:
        return number
    if isinstance(number, int):
        return number + value
    return [add_to_leftmost(number[0], value), number[1]]


def add_to_rightmost(number, value):
    if value is None:
        return number
    if isinstance(number, int):
        return number + value
    return [number[0], add_to_rightmost(number[1], value)]


def explode(number, depth=0) -> Tuple[int, Explosion]:
    if isinstance(number, int):
        return False, Explosion(None, None, number)

    if depth >= 4:
        return True, Explosion(*number, 0)

    lhs, rhs = number
    changed, result = explode(lhs, depth + 1)
    if changed:
        return True, Explosion(
            result.left, None, [result.value, add_to_leftmost(rhs, result.right)]
        )
    # LHS didn't change so it's just the value
    lhs = unwrap(result.value)

    changed, result = explode(rhs, depth + 1)
    if changed:
        return True, Explosion(
            None, result.right, [add_to_rightmost(lhs, result.left), result.value]
        )

    return False, Explosion(None, None, number)


def split(number):
    if isinstance(number, int):
        if number >= 10:
            return True, [number // 2, math.ceil(number / 2)]
        return False, number

    lhs, rhs = number
    changed, lhs = split(lhs)
    if changed:
        return True, [lhs, rhs]

    changed, rhs = split(rhs)
    return changed, [lhs, rhs]


def magnitude(number):
    if isinstance(number, int):
        return number
    return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


def solve(input: str) -> Generator[any, None, None]:
    numbers = [eval(line) for line in input.split("\n")]

    yield magnitude(reduce(snailfish_add, numbers))
    yield max(
        magnitude(snailfish_add(a, b)) for a, b in itertools.permutations(numbers, 2)
    )
