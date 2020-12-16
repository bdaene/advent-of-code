from collections import Counter, defaultdict

from utils import timeit


@timeit
def get_adaptors():
    with open('input.txt') as input_file:
        return list(int(line) for line in input_file)


@timeit
def part_1(adaptors):
    joltages = [0] + adaptors + [adaptors[-1] + 3]
    distribution = Counter(b - a for a, b in zip(joltages, joltages[1:]))
    print(distribution)
    return distribution[1] * distribution[3]


@timeit
def part_2(adaptors):
    ways = defaultdict(int)
    ways[0] = 1

    for adaptor in adaptors:
        ways[adaptor] = sum(ways[joltage] for joltage in range(adaptor - 3, adaptor))

    return ways[adaptors[-1]]


def main():
    adaptors = get_adaptors()
    adaptors.sort()
    part_1(adaptors)
    part_2(adaptors)


if __name__ == "__main__":
    main()
