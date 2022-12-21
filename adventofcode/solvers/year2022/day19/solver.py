from typing import Generator
from collections import defaultdict as dd
from collections import deque
import numpy as np
import networkx as nx
import re, math, itertools


def simulate_blueprint(
    ore_cost: int,
    clay_ore_cost: int,
    obs_ore_cost: int,
    obs_clay_cost: int,
    geo_ore_cost: int,
    geo_obs_cost: int,
    total_time: int,
):
    num_geodes = 0

    MAX_ORE = max(ore_cost, clay_ore_cost, obs_ore_cost, geo_ore_cost)

    starting_state = (1, 0, 0, 0, 0, 0, 0, 0, total_time)
    queue = deque([starting_state])
    all_states = set()

    while queue:
        (
            ore_bots,
            clay_bots,
            obs_bots,
            geo_bots,
            ore,
            clay,
            obsidian,
            geodes,
            time_left,
        ) = queue.popleft()

        assert (
            ore_bots <= MAX_ORE
            and clay_bots <= obs_clay_cost
            and obs_bots <= geo_obs_cost
        )

        num_geodes = max(num_geodes, geodes)
        if time_left == 0:
            continue

        ore = min(ore, MAX_ORE * time_left - ore_bots * (time_left - 1))
        clay = min(clay, obs_clay_cost * time_left - clay_bots * (time_left - 1))
        obsidian = min(obsidian, geo_obs_cost * time_left - obs_bots * (time_left - 1))

        state = (
            ore_bots,
            clay_bots,
            obs_bots,
            geo_bots,
            ore,
            clay,
            obsidian,
            geodes,
            time_left,
        )

        if state in all_states:
            # We already know this subproblem
            continue

        # Otherwise, we do the subproblem
        all_states.add(state)

        # Option 1: do nothing
        queue.append(
            (
                ore_bots,
                clay_bots,
                obs_bots,
                geo_bots,
                ore + ore_bots,
                clay + clay_bots,
                obsidian + obs_bots,
                geodes + geo_bots,
                time_left - 1,
            )
        )

        # Option 2: build ore bot
        if ore_bots < MAX_ORE and ore >= ore_cost:
            queue.append(
                (
                    ore_bots + 1,
                    clay_bots,
                    obs_bots,
                    geo_bots,
                    ore - ore_cost + ore_bots,
                    clay + clay_bots,
                    obsidian + obs_bots,
                    geodes + geo_bots,
                    time_left - 1,
                )
            )

        # Option 3: build clay bot
        if clay_bots < obs_clay_cost and ore >= clay_ore_cost:
            queue.append(
                (
                    ore_bots,
                    clay_bots + 1,
                    obs_bots,
                    geo_bots,
                    ore - clay_ore_cost + ore_bots,
                    clay + clay_bots,
                    obsidian + obs_bots,
                    geodes + geo_bots,
                    time_left - 1,
                )
            )

        # Option 4: build obsidian bot
        if obs_bots < geo_obs_cost and ore >= obs_ore_cost and clay >= obs_clay_cost:
            queue.append(
                (
                    ore_bots,
                    clay_bots,
                    obs_bots + 1,
                    geo_bots,
                    ore - obs_ore_cost + ore_bots,
                    clay - obs_clay_cost + clay_bots,
                    obsidian + obs_bots,
                    geodes + geo_bots,
                    time_left - 1,
                )
            )

        # Option 5: build geode bot
        if ore >= geo_ore_cost and obsidian >= geo_obs_cost:
            queue.append(
                (
                    ore_bots,
                    clay_bots,
                    obs_bots,
                    geo_bots + 1,
                    ore - geo_ore_cost + ore_bots,
                    clay + clay_bots,
                    obsidian - geo_obs_cost + obs_bots,
                    geodes + geo_bots,
                    time_left - 1,
                )
            )
    return num_geodes


def solve(inp: str) -> Generator[any, None, None]:

    blueprints = []
    for line in inp.split("\n"):
        parts = line.split(".")
        ore = int(re.search(r"(\d+) ore", parts[0]).group(1))
        clay = int(re.search(r"(\d+) ore", parts[1]).group(1))
        match = re.search(r"(\d+) ore and (\d+) clay", parts[2])
        obsidian = (int(match.group(1)), int(match.group(2)))
        match = re.search(r"(\d+) ore and (\d+) obsidian", parts[3])
        geode = (int(match.group(1)), int(match.group(2)))

        blueprints.append((ore, clay, *obsidian, *geode))

    quality = 0
    for i, bp in enumerate(blueprints, 1):
        num_geodes = simulate_blueprint(*bp, 24)
        print(f"{i}:\t{num_geodes}")
        quality += i * num_geodes

    # Part 1
    yield int(quality)

    # Part 2
    answer = 1
    for i, bp in enumerate(blueprints[:3], 1):
        num_geodes = simulate_blueprint(*bp, 32)
        print(f"{i}:\t{num_geodes}")
        answer *= num_geodes
    yield answer
