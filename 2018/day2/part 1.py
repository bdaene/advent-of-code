

from collections import Counter


def solve(input_file):
    count2, count3 = 0, 0
    for line in input_file:
        count = Counter(line)
        if 2 in count.values():
            count2 += 1
        if 3 in count.values():
            count3 += 1
    ans = count2 * count3
    return ans


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))