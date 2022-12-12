
def get_int_list(filename="input.txt"):
    lst = []
    with open(filename, 'r') as f:
        for line in f:
            lst.append(int(line))
    return lst

def get_line_list(filename="input.txt"):
    lst = []
    with open(filename, 'r') as f:
        for line in f:
            lst.append(line)
    return lst

def slope(right, down, trees):
    i = 0
    j = 0
    total = 0
    while i < len(trees):
        row = trees[i].strip()
        if row[j] == "#":
            total += 1
        j = (j + right) % len(row)
        i += down
    return total

def main():
    trees = get_line_list()

    total = slope(1,1,trees) * slope(3,1,trees) * slope(5,1,trees) * slope(7,1,trees) * slope(1,2,trees)

    return total

print(main())