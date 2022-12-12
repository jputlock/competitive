from math import log10, ceil

def get_digit(number, place):
    return number // (10 ** place) % 10

def solve():
    n = int(input())

    order = ceil(log10(n))
    
    a, b = 0, 0

    for place in range(order + 1):
        to_add = 10 ** (place // 2) * get_digit(n, place)

        if place % 2 == 0:
            a += to_add
        else:
            b += to_add

    return (a + 1) * (b + 1) - 2

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()