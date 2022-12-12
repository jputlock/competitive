from typing import Generator

import numpy as np


def mark_number(board, marker, number):
    indices = np.where(board == number)
    marker[indices] = True


def is_win(mark):
    for i in range(5):
        if np.all(mark[i, :] == True) or np.all(mark[:, i] == True):
            return True
    return False


def solve(input: str) -> Generator[any, None, None]:
    lines = [line.strip() for line in input.split("\n") if line]

    numbers = [int(x) for x in lines[0].split(",")]

    boards = []
    marks = []

    line_num = 1
    while line_num < len(lines):
        board = np.array(
            [[int(x) for x in lines[line_num + i].split()] for i in range(5)]
        ).reshape((5, 5))
        mark = np.array([False] * 25, dtype=bool).reshape((5, 5))

        boards.append(board)
        marks.append(mark)

        line_num += 5

    indices = list(range(len(boards)))

    first = True

    for number in numbers:
        i = 0
        while i < len(indices):
            index = indices[i]
            board, mark = boards[index], marks[index]
            mark_number(board, mark, number)

            if is_win(mark):
                if first or len(indices) == 1:
                    if first:
                        first = False
                    yield int(np.sum(board[np.where(mark == False)])) * number
                indices.remove(index)
            else:
                i += 1
