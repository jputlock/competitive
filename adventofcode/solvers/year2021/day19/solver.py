from typing import Generator
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

axis_ordering = list(itertools.permutations(range(3)))
axis_negations = list(itertools.product([-1, 1], [-1, 1], [-1, 1]))


def transform_scans(order: list, negation: list, scanner: list):
    return [[a * scan[b] for a, b in zip(negation, order)] for scan in scanner]


def find_alignment(aligned_scanner: list, new_scanner: list, dists_from_origin: list):
    # These are the "actual" beacon coordinates
    aligned_beacons = set([tuple(x) for x in aligned_scanner])

    # Try every possible alignment of rotatings and facings
    for order in axis_ordering:
        for negation in axis_negations:
            transformed_scanner = transform_scans(order, negation, new_scanner)

            # Check every pair of scans
            for scan_a in aligned_scanner:
                for scan_b in transformed_scanner:
                    # The difference between the two (post alignment) is the
                    # actual location of the new scanner
                    diff = tuple(b - a for a, b in zip(scan_a, scan_b))

                    # Get the actual locations of the beacons for the new scanner
                    transformed = [
                        [x - d for x, d in zip(scan, diff)]
                        for scan in transformed_scanner
                    ]

                    # Count how many of these beacons match with the 'correct'
                    matches = sum(
                        tuple(transformed) in aligned_beacons
                        for transformed in transformed
                    )

                    # If we have enough, then it's a match
                    if matches >= 12:
                        print("match", diff)
                        dists_from_origin.append(diff)
                        return transformed
    return None


def solve(input: str) -> Generator[any, None, None]:
    scanners = [
        [eval(f"[{coord}]") for coord in scan.split("\n") if coord]
        for scan in re.split(r"-+ scanner \d+ -+\n", input)[1:]
    ]

    aligned_scanners = set([0])
    final_alignments = {0: scanners[0]}
    final_beacons = set(tuple(x) for x in scanners[0])
    dists_from_origin = [(0, 0, 0)]

    already_checked = set()
    # While there are still scanners to align
    while len(aligned_scanners) < len(scanners):
        for index in range(len(scanners)):
            if index in aligned_scanners:
                continue
            # index is the next unaligned scanner
            for aligned_index in aligned_scanners:
                if (index, aligned_index) in already_checked:
                    continue

                print(f"({index:2d},{aligned_index:2d})")

                # Attempt to align index with any already aligned scanner
                alignment = find_alignment(
                    final_alignments[aligned_index], scanners[index], dists_from_origin
                )

                # If they align, then save that
                if alignment:
                    aligned_scanners.add(index)
                    final_alignments[index] = alignment
                    final_beacons.update(tuple(x) for x in alignment)
                    break

                # Otherwise note that we already did this
                already_checked.add((index, aligned_index))

    yield len(set(final_beacons))

    dists = [
        sum([abs(x - y) for x, y in zip(a, b)])
        for a, b in itertools.permutations(dists_from_origin, 2)
    ]

    yield max(dists)
