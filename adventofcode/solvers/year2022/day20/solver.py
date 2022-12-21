from typing import Generator, Optional
from collections import defaultdict as dd
import numpy as np
import networkx as nx
import re, math, itertools

offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Node:
    def __init__(self, val):
        self.value: int = val
        self.prev: Node = self
        self.next: Node = self


class LinkedList:
    def __init__(self, vals: list, index_map: dict):
        self.head: Optional[Node] = None
        prev: Optional[Node] = None
        current: Optional[Node] = None

        for i, val in enumerate(vals):
            current = Node(val)
            current.prev = prev

            if self.head is None:
                self.head = current
            if prev is not None:
                prev.next = current

            index_map[i] = current

            prev = current
        # Make it circular
        self.head.prev = current
        current.next = self.head
        self.len = len(vals)

    def move(self, node: Node, amount: int):
        # Remove this node from the list
        node.prev.next = node.next
        node.next.prev = node.prev

        # Calculate the displacement in a list without this element
        amount = amount % (self.len - 1)

        # Calculate the node before where this should be re-inserted
        curr = node.prev
        for _ in range(amount):
            curr = curr.next

        # Fix this node's pointers
        node.prev = curr
        node.next = curr.next

        # Fix the surrounding node pointers
        curr.next.prev = node
        curr.next = node


def solve(input: str) -> Generator[any, None, None]:

    # Part 1
    vals = [int(line.strip()) for line in input.split("\n") if line]
    mymap = {}
    myll = LinkedList(vals, mymap)
    for i, val in enumerate(vals):
        myll.move(mymap[i], val)

    zero_index = vals.index(0)
    zero = mymap[zero_index]
    moveby = 1000 % myll.len

    total = 0
    current = zero
    for i in range(3):
        for _ in range(moveby):
            current = current.next
        total += current.value
    yield total

    # Part 2
    vals = [x * 811589153 for x in vals]
    mymap = {}

    myll = LinkedList(vals, mymap)

    for _ in range(10):
        for i, val in enumerate(vals):
            myll.move(mymap[i], val)

    zero_index = vals.index(0)
    zero = mymap[zero_index]
    moveby = 1000 % myll.len

    total = 0
    current = zero
    for i in range(3):
        for _ in range(moveby):
            current = current.next
        total += current.value

    # Part 1
    yield total
