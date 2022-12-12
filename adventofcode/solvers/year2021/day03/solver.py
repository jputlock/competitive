from typing import Generator


def solve(input: str) -> Generator[any, None, None]:
    instructions = [line.strip() for line in input.split("\n") if line]
    length = len(instructions[0])
    num_instructions = len(instructions)

    # Part 1
    most_common_bits = [
        str(int(sum(x[i] == "1" for x in instructions) > num_instructions // 2))
        for i in range(length)
    ]
    least_common_bits = [str(1 - int(x)) for x in most_common_bits]
    gamma = int("".join(most_common_bits), base=2)
    epsilon = int("".join(least_common_bits), base=2)

    yield gamma * epsilon

    # Part 2

    oxy_working = instructions.copy()
    co2_working = instructions.copy()

    for bit_index in range(length):
        most_common = str(
            int(sum(x[bit_index] == "1" for x in oxy_working) >= len(oxy_working) // 2)
        )
        oxy_working = [x for x in oxy_working if x[bit_index] == most_common]

        if len(oxy_working) == 1:
            break

    oxy = int(oxy_working[0], base=2)

    for bit_index in range(length):
        least_common = str(
            int(sum(x[bit_index] == "1" for x in co2_working) < len(co2_working) // 2)
        )
        co2_working = [x for x in co2_working if x[bit_index] == least_common]
        if len(co2_working) == 1:
            break

    co2 = int(co2_working[0], base=2)

    yield oxy * co2
