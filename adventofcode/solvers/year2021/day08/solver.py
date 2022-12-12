from typing import *
from collections import defaultdict as dd
import numpy as np
import re
import itertools


possibilities = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]

letter_pool = "abcdefg"


def decode_line(line: str):
    print("HELLO")
    befores, afters = line.split(" | ")
    befores = befores.split(" ")
    afters = afters.split(" ")

    for permutation in itertools.permutations():
        mapping = {a: b for a, b in zip(permutation, letter_pool)}
        print(befores)
        decoded_before = [
            "".join(sorted([mapping[letter] for letter in word])) for word in befores
        ]
        print(decoded_before)
        decoded_after = [
            "".join(sorted([mapping[letter] for letter in word])) for word in afters
        ]
        print(decoded_after)

        if all(decoded in possibilities for decoded in decoded_before):
            yield possibilities.index("1")


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    # Part 1
    # befores = []
    # afters = []
    # for line in lines:
    #     print(line)
    #     a, b = line.split(" | ")
    #     befores.append(a.split(" "))
    #     afters.append(b.split(" "))

    # num on -> possible numbers

    # counter = 0
    # for lst in afters:
    #     for word in lst:
    #         if len(word) == 2 or len(word) == 3 or len(word) == 4 or len(word) == 7:
    #             counter += 1
    # yield counter

    # Part 2
    total = 0
    for line in lines:
        befores, afters = line.split(" | ")
        befores = befores.split(" ")
        afters = afters.split(" ")

        for permutation in itertools.permutations(letter_pool):
            mapping = {a: b for a, b in zip(permutation, letter_pool)}
            decoded_before = [
                "".join(sorted([mapping[letter] for letter in word]))
                for word in befores
            ]

            if all(decoded in possibilities for decoded in decoded_before):
                decoded_after = [
                    "".join(sorted([mapping[letter] for letter in word]))
                    for word in afters
                ]
                output = [str(possibilities.index(word)) for word in decoded_after]
                total += int("".join(output))
    yield total
