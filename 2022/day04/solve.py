import re
from dataclasses import dataclass

from utils import timeit


@dataclass
class Range:
    start: int
    end: int

    def contains_fully(self, other: 'Range'):
        return self.start <= other.start and other.end <= self.end

    def overlaps(self, other):
        return self.start <= other.end and other.start <= self.end


@timeit
def get_data():
    data = []
    pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            a, b, c, d = map(int, pattern.fullmatch(line.strip()).groups())
            data.append((Range(a, b), Range(c, d)))
    return data


@timeit
def part_1(data):
    return sum(range_1.contains_fully(range_2) or range_2.contains_fully(range_1) for range_1, range_2 in data)


@timeit
def part_2(data):
    return sum(range_1.overlaps(range_2) for range_1, range_2 in data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
