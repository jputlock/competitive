def solve():
    n = int(input())
    s = input()

    answer = []

    for c in s:
        if c == "L" or c == "R":
            answer += [c]
        elif c == "U":
            answer += ["D"]
        elif c == "D":
            answer += ["U"]


    return "".join(answer)

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(f"{solve()}")

if __name__ == "__main__":
    main()