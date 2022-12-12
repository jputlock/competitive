import math

def create_split(s, n):

    if n == 1:
        return [s]

    # get biggest power of 10
    order = math.floor(math.log10(s))
    chunk = 10 ** order

    while s - chunk < n - 1:
        order -= 1
        chunk //= 10

    return [chunk] + create_split(s - chunk, n - 1)

def solve():
    s, n = [int(x) for x in input().split(' ')]

    sol_set = create_split(s, n)

    return " ".join(str(x) for x in sol_set)

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()