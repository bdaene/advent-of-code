import re

from matplotlib import pyplot
from utils import timeit


@timeit
def get_data():
    data = []
    pattern = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            sx, sy, bx, by = map(int, pattern.fullmatch(line.strip()).groups())
            data.append(((sx, sy), (bx, by)))
    return tuple(data)


def show(data):
    pyplot.plot([sx for (sx, sy), b in data], [sy for (sx, sy), b in data], '*')
    pyplot.plot([bx for s, (bx, by) in data], [by for s, (bx, by) in data], '+')

    for (sx, sy), (bx, by) in data:
        dist = abs(bx - sx) + abs(by - sy)
        pyplot.fill([sx - dist, sx, sx + dist, sx, sx - dist], [sy, sy - dist, sy, sy + dist, sy], 'r-')

    pyplot.show()


def get_impossible_ranges(data, y):
    impossible_ranges = []
    for (sx, sy), (bx, by) in data:
        distance = abs(bx - sx) + abs(by - sy)
        delta = distance - abs(y - sy)
        if delta < 0:
            continue
        impossible_ranges.append((sx - delta, sx + delta))
    return impossible_ranges


def get_gaps(ranges):
    gaps = []
    if not ranges:
        return gaps
    ranges.sort()
    end = ranges[0][0]-1
    for left, right in ranges:
        if left > end + 1:
            gaps.append((end+1, left-1))
        end = max(end, right)
    return gaps


@timeit
def part_1(data, y=2000000):
    impossible_ranges = get_impossible_ranges(data, y)
    objects_on_line = set(s for s, b in data if s[1] == y) | set(b for s, b in data if b[1] == y)

    gaps = get_gaps(impossible_ranges)

    return (max(right for left, right in impossible_ranges) - min(left for left, right in impossible_ranges) + 1
            - sum(right - left + 1 for left, right in gaps)
            - len(objects_on_line)
            )


@timeit
def part_2(data, max_y=4000000):
    for y in range(max_y+1):
        gaps = get_gaps(get_impossible_ranges(data, y))
        if gaps:
            print(gaps, y)
            for gap in gaps:
                for x in range(gap[0], gap[1]+1):
                    print(x * 4000000 + y)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
