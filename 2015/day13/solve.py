import re
from collections import defaultdict

from itertools import permutations
from utils import timeit


@timeit
def get_happiness():
    happiness = defaultdict(dict)
    pattern = re.compile(r'(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).')
    with open('input.txt') as input_file:
        for line in input_file:
            a, s, v, b = pattern.match(line).groups()
            happiness[a][b] = int(v) if s == 'gain' else -int(v)
    return happiness


@timeit
def part_1(happiness):
    guests = tuple(happiness.keys())
    guest_0 = guests[0]
    best = 0
    for table in permutations(guests[1:]):
        table_happiness = sum(
            happiness[a][b] + happiness[b][a] for a, b in zip((guest_0,) + table, table + (guest_0,)))
        best = max(best, table_happiness)

    return best


@timeit
def part_2(happiness):
    guests = tuple(happiness.keys())
    best = 0
    for table in permutations(guests):
        table_happiness = sum(happiness[a][b] + happiness[b][a] for a, b in zip(table[1:], table[:-1]))
        best = max(best, table_happiness)

    return best


def main():
    happiness = get_happiness()
    part_1(happiness)
    part_2(happiness)


if __name__ == "__main__":
    main()
