def solve():
    n = int(input())
    s = input()

    ab = 0
    for i, c in enumerate(s, 1):
        if c == "a":
            if ab < 0:
                return f"{i-1} {i}"
            ab += 1
        else:
            if ab > 0:
                return f"{i-1} {i}"
            ab -= 1

    return "-1 -1"

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()