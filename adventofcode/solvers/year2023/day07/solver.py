from typing import *
import collections
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

HandTuple = Tuple[str, str, int]

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
PAIR = 2
HIGH_CARD = 1

CARDS = "23456789TJQKA"


# Part 1


def rate(x: HandTuple):
    hand, _, handtype = x
    magnitude = 1
    rating = 0
    for card in reversed(hand):
        rating += CARDS.index(card) * magnitude
        magnitude *= len(CARDS)
    rating += handtype * magnitude
    return rating


def get_type(hand: str) -> int:
    counter = collections.Counter(hand)

    if len(counter) == 1:
        return FIVE_OF_A_KIND
    elif len(counter) == 2:
        if 4 in counter.values():
            return FOUR_OF_A_KIND
        else:
            return FULL_HOUSE
    elif len(counter) == 3:
        if 3 in counter.values():
            return THREE_OF_A_KIND
        else:
            return TWO_PAIR
    elif len(counter) == 4:
        return PAIR
    # else:
    return HIGH_CARD


# Part 2

NEW_CARDS = "J23456789TQKA"


def rate_new(x: HandTuple):
    hand, _, handtype = x
    magnitude = 1
    rating = 0
    for card in reversed(hand):
        rating += NEW_CARDS.index(card) * magnitude
        magnitude *= len(NEW_CARDS)
    rating += handtype * magnitude
    return rating


def get_type_new(hand: str) -> int:
    counter = collections.Counter(hand)

    if "J" in counter and len(counter) > 1:
        max_val = max(val for key, val in counter.items() if key != "J")
        max_key = sorted(
            [key for key, val in counter.items() if val == max_val and key != "J"],
            key=NEW_CARDS.index,
        )[-1]
        counter[max_key] += counter["J"]
        del counter["J"]

    if len(counter) == 1:
        return FIVE_OF_A_KIND
    elif len(counter) == 2:
        if 4 in counter.values():
            return FOUR_OF_A_KIND
        else:
            return FULL_HOUSE
    elif len(counter) == 3:
        if 3 in counter.values():
            return THREE_OF_A_KIND
        else:
            return TWO_PAIR
    elif len(counter) == 4:
        return PAIR
    # else:
    return HIGH_CARD


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    # Part 1
    hands, bids = list(map(list, zip(*[line.split() for line in lines])))
    types: list[int] = list(map(get_type, hands))
    ans = sorted(zip(hands, bids, types), key=rate)
    yield sum(spot * int(bid) for spot, (_, bid, _) in enumerate(ans, 1))

    types: list[int] = list(map(get_type_new, hands))
    ans = sorted(zip(hands, bids, types), key=rate_new)
    yield sum(spot * int(bid) for spot, (_, bid, _) in enumerate(ans, 1))
