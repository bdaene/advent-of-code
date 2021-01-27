from collections import Counter
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


@timeit
def part_1(data):
    count = [Counter(column) for column in zip(*data)]
    return ''.join(max(c, key=c.get) for c in count)


@timeit
def part_2(data):
    count = [Counter(column) for column in zip(*data)]
    return ''.join(min(c, key=c.get) for c in count)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
