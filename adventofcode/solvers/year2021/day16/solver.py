from typing import Generator
from collections import defaultdict as dd
from collections import deque
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

versum = 0


def decode(binstring: str):
    global versum

    version = int(binstring[:3], 2)
    versum += version

    type_id = int(binstring[3:6], 2)
    working = binstring[6:]

    if type_id == 4:
        literal = ""
        while True:
            start = working[0]
            literal += working[1:5]
            working = working[5:]
            if start == "0":
                break
        return working, int(literal, 2)
    else:
        length_id = working[0]
        values = []

        if length_id == "0":
            length = int(working[1:16], 2)
            working = working[16:]
            subpackets = working[:length]
            while subpackets:
                subpackets, value = decode(subpackets)
                values.append(value)
            working = working[length:]
        else:
            num_subs = int(working[1:12], 2)
            working = working[12:]
            for _ in range(num_subs):
                working, value = decode(working)
                values.append(value)

        if type_id == 0:
            return (working, sum(values))
        elif type_id == 1:
            return (working, math.prod(values))
        elif type_id == 2:
            return (working, min(values))
        elif type_id == 3:
            return (working, max(values))
        elif type_id == 5:
            return (working, int(values[0] > values[1]))
        elif type_id == 6:
            return (working, int(values[0] < values[1]))
        elif type_id == 7:
            return (working, int(values[0] == values[1]))

    return working


def solve(input: str) -> Generator[any, None, None]:
    line = input.strip()
    hex_line = int(line, 16)
    bin_line = f"{hex_line:b}"

    # Part 1
    a = decode(bin_line)
    yield versum
    yield a[1]
