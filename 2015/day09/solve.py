import re
from collections import defaultdict
from heapq import heappush, heappop, heapify

from utils import timeit


@timeit
def get_distances():
    distances = defaultdict(dict)
    pattern = re.compile(r'(\w+) to (\w+) = (\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            a, b, d = pattern.match(line).groups()
            d = int(d)
            distances[a][b] = d
            distances[b][a] = d
    return distances


@timeit
def part_1(distances):
    locations = frozenset(distances.keys())
    stack = [(0, location, locations - {location}) for location in locations]
    heapify(stack)

    while len(stack) > 0:
        distance, location, to_visit = heappop(stack)
        if len(to_visit) == 0:
            return distance
        for visit in to_visit:
            heappush(stack, (distance + distances[location][visit], visit, to_visit - {visit}))


@timeit
def part_2(distances):
    locations = frozenset(distances.keys())
    stack = [(1, 0, location, locations - {location}) for location in locations]
    heapify(stack)

    while len(stack) > 0:
        visited, distance, location, to_visit = heappop(stack)
        if len(to_visit) == 0:
            return -distance
        for visit in to_visit:
            heappush(stack, (visited + 1, distance - distances[location][visit], visit, to_visit - {visit}))


def main():
    distances = get_distances()
    part_1(distances)
    part_2(distances)


if __name__ == "__main__":
    main()
