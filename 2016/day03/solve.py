from utils import timeit
from itertools import chain


@timeit
def get_data():
    with open('input.txt') as input_file:
        return [tuple(map(int, line.split())) for line in input_file]


@timeit
def part_1(data):
    return sum(1 for sides in data if 2*max(sides) < sum(sides))


@timeit
def part_2(data):
    values = list(chain.from_iterable(zip(*data)))
    triangles = [values[i:i+3] for i in range(0, len(values), 3)]

    return sum(1 for sides in triangles if 2 * max(sides) < sum(sides))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
