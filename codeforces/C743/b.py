def solve():
    n = int(input())
    arr_a = [int(x) for x in input().split(" ")]
    arr_b = [int(x) for x in input().split(" ")]

    # dist[val] = minimum dist to get at most val as head of arr_a
    dist = [n] * (n+1)

    for i, val in enumerate(arr_a):
        for j in range((val - 1) // 2, n):
            if dist[j] < i:
                break
            dist[j] = min(dist[j], i)

    ans = 2 * n

    for i, val in enumerate(arr_b):
        ans = min(ans, i + dist[val//2 - 1])

    return ans

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()