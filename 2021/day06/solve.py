from collections import Counter
from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(map(int, input_file.readline().split(',')))


@timeit
def part_1(data, days=80):
    counters = Counter(data)
    for _ in range(days):
        counters = {counter-1: number for counter, number in counters.items()}
        if -1 in counters:
            counters[8] = counters.pop(-1)
            counters[6] = counters.get(6, 0) + counters[8]

    return sum(counters.values())


@timeit
def part_2(data):
    return part_1.func(data, days=256)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
