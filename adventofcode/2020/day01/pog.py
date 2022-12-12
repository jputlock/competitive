
def parse_file(filename):
    lst = []
    with open(filename, 'r') as f:
        for line in f:
            lst.append(int(line))
    return lst

def main():

    lst = parse_file("input.txt")

    for i in range(len(lst)):
        s = set()
        curr_sum = 2020 - lst[i]

        for j in range(i+1, len(lst)):
            if curr_sum - lst[j] in s:
                return lst[i] * lst[j] * (curr_sum - lst[j])
            s.add(lst[j])


print(main())