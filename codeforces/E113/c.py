from collections import defaultdict
from math import factorial

def solve():
    n = int(input())
    count = defaultdict(int)
    for x in input().split(" "):
        intx = int(x)
        count[intx] += 1

    sortedkeys = sorted(count.keys(), reverse=True)
<<<<<<< HEAD
    if len(sortedkeys) > 1 and sortedkeys[0] - sortedkeys[1] >= 2:
        return "0"

    largest_key = sortedkeys[0]
    k = count[largest_key]
    
    prod = factorial(n)
    if len(sortedkeys) == 1:
        return str(prod)
    
    second_largest_key = sortedkeys[1]
    k2 = count[second_largest_key]

    if k == 1:
        prod *= n * (n + 1) // 2
        prod //= (n - k2 + 2) * (n - k2 + 1)

    prod %= 998_244_353

    return str(prod)
=======
    for i in range(1, len(sortedkeys)):
        if sortedkeys[i] - sortedkeys[i-1] >= 2:
            return "0"

    largest_key = sortedkeys[0]
    k = count[largest_key]

    if k > 1:
        prod = factorial(n)
        for key in sortedkeys:
            prod //= factorial(count[key])
        return str(prod % 998_244_353)

    prod = factorial(n-1)
    for i, key in enumerate(sortedkeys):
        cnt = count[key]
        if i <= 1:
            cnt -= 1
        prod //= factorial(cnt)

    return str(prod % 998_244_353)
>>>>>>> 623bce8 (fuck)

    
    


def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()