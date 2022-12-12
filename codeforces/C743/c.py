from collections import defaultdict, deque
import sys
input = sys.stdin.readline


def solve():
    num_chapters = int(input())
    graph = defaultdict(set)
    d_in = defaultdict(int)

    for chapter in range(1, num_chapters+1):
        line = list(map(int, input().split(" ")))
        d_in[chapter] += line[0]
        
        for j in range(1, line[0] + 1):
            graph[line[j]].add(chapter)

    # graph in the form:
    # node -> set(required nodes)

    return has_loop(graph, d_in, num_chapters)

def has_loop(graph, d_in, num_chapters):
    counter = 0
    queue = deque([])
    
    dists = defaultdict(lambda: 1)

    # gather the unrequired nodes
    for i in range(1, num_chapters + 1):
        if d_in[i] == 0:
            queue.append(i)

    while queue:
        current = queue.popleft()
        counter += 1

        for neighbor in graph[current]:
            d_in[neighbor] -= 1
            if neighbor < current:
                dists[neighbor] = max(dists[neighbor], dists[current] + 1)
            else:
                dists[neighbor] = max(dists[neighbor], dists[current])
            if d_in[neighbor] == 0:
                queue.append(neighbor)

    if counter != num_chapters:
        return -1
    if dists:
        return max(dists.values())
    return 1    

def main():
    num_tests = int(input())
    for t in range(1, num_tests+1):
        print(solve())

if __name__ == "__main__":
    main()