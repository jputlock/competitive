
def get_int_list():
    lst = []
    with open(filename, 'r') as f:
        for line in f:
            lst.append(int(line))
    return lst

def get_line_list(filename):
    lst = []
    with open(filename, 'r') as f:
        for line in f:
            lst.append(line)
    return lst

def main():
    lst = get_line_list("input.txt")
    total = 0
    for line in lst:
        broken = line.split(" ")
        nums = broken[0].split("-")
        first, second = int(nums[0]) - 1, int(nums[1]) - 1

        letter = broken[1][0]

        passwd = broken[2]

        occur = 0

        if (passwd[first] == letter) ^ (passwd[second] == letter):
            total += 1
    return total

print(main())