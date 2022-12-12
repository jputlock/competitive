
from collections import defaultdict
from math import sqrt

def discrete_log(a, b, m):
    
    n = int(sqrt(m) + 1)

    an = pow(a, n, m)
    ani = defaultdict(int)

    current = an
    for i in range(1, n + 1):
        if ani[current] != 0:
            break
        # if we ever have same value, it's in a cycle
        ani[current] = i
        current = (current * an) % m
    
    current = b
    for j in range(n + 1):
        if ani[current] > 0:
            ans = ani[current] * n - j
            if ans < m:
                return ans
            else:
                print("cringe")
        current = (current * a) % m
    
    return -1
