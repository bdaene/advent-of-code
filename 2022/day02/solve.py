from enum import Enum

from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(tuple(line.split()) for line in input_file)


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def get_score(self, other):
        return ((self.value - other.value + 1) % 3) * 3 + self.value

    def get_shape(self, round_result):
        return Shape((self.value + 'YZX'.index(round_result) - 1) % 3 + 1)


@timeit
def part_1(data):
    left = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
    right = {'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSORS}
    return sum(right[b].get_score(left[a]) for a, b in data)


@timeit
def part_2(data):
    left = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
    return sum(left[a].get_shape(b).get_score(left[a]) for a, b in data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
