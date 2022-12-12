def solve():
    n = int(input())
    x = input()
    ans = sum(int(dig) + (n - i > 1) if int(dig) > 0 else 0 for i, dig in enumerate(x))

    return ans

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()