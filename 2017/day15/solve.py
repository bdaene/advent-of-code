import re
from itertools import islice
from utils import timeit


@timeit
def get_data():
    data = {}
    pattern = re.compile(r'Generator (\w+) starts with (\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            generator, seed = pattern.match(line).groups()
            data[generator] = int(seed)
    return data


@timeit
def part_1(data, ):

    mod = 2147483647

    def gen_values(seed, factor):
        while True:
            seed = (seed * factor) % mod
            yield seed

    mask = 0xffff
    matches = 0
    for a, b in islice(zip(gen_values(data['A'], 16807), gen_values(data['B'], 48271)), 40000000):
        if (a & mask) == (b & mask):
            matches += 1

    return matches


@timeit
def part_2(data):

    mod = 2147483647

    def gen_values(seed, factor, criteria):
        while True:
            seed = (seed * factor) % mod
            if not (seed & criteria):
                yield seed

    mask = 0xffff
    count, matches = 0, 0
    for a, b in islice(zip(gen_values(data['A'], 16807, 0x3), gen_values(data['B'], 48271, 0x7)), 5000000):
        if (a & mask) == (b & mask):
            matches += 1

    return matches


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
