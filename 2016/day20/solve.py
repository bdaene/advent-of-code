import re
from bisect import bisect
from utils import timeit


@timeit
def get_data():
    data = []
    pattern = re.compile(r'(\d+)-(\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            a, b = pattern.match(line).groups()
            data.append((int(a), int(b)))
    return data


class RangesUnion:

    def __init__(self):
        self.ranges = []

    def add_range(self, a, b):
        i = bisect(self.ranges, (a, b))
        if i > 0 and self.ranges[i-1][1] >= a:
            i -= 1
            a = min(a, self.ranges[i][0])
            b = max(b, self.ranges[i][1])
            del self.ranges[i]
        while i < len(self.ranges) and self.ranges[i][0] <= b:
            a = min(a, self.ranges[i][0])
            b = max(b, self.ranges[i][1])
            del self.ranges[i]
        self.ranges.insert(i, (a, b))


@timeit
def part_1(data):

    ranges = RangesUnion()
    for a, b in data:
        ranges.add_range(a, b+1)

    if ranges.ranges[0][0] > 0:
        return 0
    else:
        return ranges.ranges[0][1]


@timeit
def part_2(data):

    ranges = RangesUnion()
    for a, b in data:
        ranges.add_range(a, b+1)

    total = 2**32
    for a, b in ranges.ranges:
        total -= b-a

    return total


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
