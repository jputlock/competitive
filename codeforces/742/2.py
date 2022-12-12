def solve():
    a, b = [int(x) for x in input().split(" ")]

    xor = 0
    n = a - 1
    if n % 4 == 0:
        xor = n
    elif n % 4 == 1:
        xor = 1
    elif n % 4 == 2:
        xor = n + 1

    if xor == b:
        return a
    elif xor ^ b != a:
        return a + 1

    return a + 2

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()