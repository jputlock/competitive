from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import sys
import re, math, itertools

INF = float("inf")

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    start = "AA"
    all_valves = set()
    valves = set()
    rates = dict()
    distances = dd(lambda: dd(lambda: INF))

    for line in lines:
        mymatch = re.search(
            r"Valve (\w+) has flow rate=(-?\d+); tunnels? leads? to valves? (.*)", line
        )
        src = mymatch.group(1)
        rate = int(mymatch.group(2))

        all_valves.add(src)
        if rate > 0:
            valves.add(src)

        rates[src] = rate
        for dst in mymatch.group(3).split(", "):
            distances[src][dst] = 1

    # Floyd-Warshall for pairwise distances
    for inter in all_valves:
        for source in all_valves:
            for sink in all_valves:
                distances[source][sink] = min(
                    distances[source][sink],
                    distances[source][inter] + distances[inter][sink],
                )

    def dfs(
        current_valve: str,
        pressure: int,
        minutes_left: int,
        opened: list,
        intermediate_sols,
    ):
        # PART 2 ONLY: Store the current state
        if isinstance(intermediate_sols, list):
            intermediate_sols.append([pressure, opened])

        # Then solve normally
        new_pressure = pressure
        for next_valve in valves:
            if next_valve is current_valve or next_valve in opened:
                continue
            dist = distances[current_valve][next_valve] + 1
            if dist <= minutes_left:
                new_pressure = max(
                    new_pressure,
                    dfs(
                        next_valve,
                        pressure + rates[next_valve] * (minutes_left - dist),
                        minutes_left - dist,
                        opened + [next_valve],
                        intermediate_sols,
                    ),
                )
        return new_pressure

    # Part 1
    yield dfs(start, 0, 30, [], None)

    # Part 2
    my_paths = []
    dfs(start, 0, 26, [], my_paths)

    yield max(
        dfs(start, my_pressure, 26, my_path, None) for my_pressure, my_path in my_paths
    )


def get_pressure(pressure, opened, rates, min_left=1):
    return pressure + sum(rates[x] for x in opened) * min_left
