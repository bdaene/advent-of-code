import re
from collections import Counter
from utils import timeit


@timeit
def get_data():
    data = []
    nanobot_pattern = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            x, y, z, r = map(int, nanobot_pattern.match(line).groups())
            data.append(((x, y, z), r))
    return data


@timeit
def part_1(data):
    best = data[0]
    for nanobot in data[1:]:
        if nanobot[1] > best[1]:
            best = nanobot

    (x, y, z), r = best
    return sum(1 for ((x_, y_, z_), r_) in data if abs(x - x_) + abs(y - y_) + abs(z - z_) <= r)


@timeit
def part_2(data):

    events = Counter()
    for (x, y, z), r in data:
        d = abs(x) + abs(y) + abs(z)
        events[max(0, d - r)] += 1
        events[d + r + 1] -= 1

    best = (0, 0)
    total = 0
    for distance, count in sorted(events.items()):
        total += count
        if total > best[1]:
            best = (distance, total)
    return best[0]


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
