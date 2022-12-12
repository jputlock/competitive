from typing import Generator


def solve(input: str) -> Generator[any, None, None]:
    instructions = [line for line in input.split("\n") if line]

    # Part 1
    h_pos, v_pos = 0, 0

    for line in instructions:
        inst, val = line.split()
        val = int(val)

        if inst == "forward":
            h_pos += val
        elif inst == "up":
            v_pos -= val
        elif inst == "down":
            v_pos += val

    yield h_pos * v_pos

    # Part 2
    h_pos, v_pos, aim = 0, 0, 0

    for line in instructions:
        parts = line.split(" ")
        inst = parts[0]
        val = int(parts[1])

        if inst == "forward":
            h_pos += val
            v_pos += aim * val
        elif inst == "up":
            aim -= val
        elif inst == "down":
            aim += val

    yield h_pos * v_pos
