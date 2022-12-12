def solve():
    n = int(input())

    expectations = [i for i, x in enumerate(input()) if x == "2"]

    # cant create a simple cycle out of 2
    if 1 <= len(expectations) <= 2:
        return "NO"

    # n(n-1) total games
    results = [
        [
            "=" if i != j else "X"
            for j in range(n)
        ]
        for i in range(n)
    ]

    # first one
    for i, node in enumerate(expectations):
        other = expectations[i - 1]
        results[node][other] = "+"
        results[other][node] = "-"

    answer = ""
    for i in range(n):
        answer += "".join(results[i]) + "\n"

    print("YES")

    return answer[:-1]

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()