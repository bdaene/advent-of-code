from functools import cache

from utils import timeit
from collections import Counter


@timeit
def get_data():
    with open('input.txt') as input_file:
        template = input_file.readline().strip()
        input_file.readline()
        rules = {pair: element for pair, element in (line.strip().split(' -> ') for line in input_file)}
    return template, rules


@timeit
def part_1(data, steps=10):
    template, rules = data
    polymer = template

    for _ in range(steps):
        polymer = polymer[0] + ''.join(f'{rules[a+b]}{b}' for a, b in zip(polymer, polymer[1:]))

    count = Counter(polymer)
    return max(count.values()) - min(count.values())


@timeit
def part_2(data, steps=40):
    template, rules = data

    @cache
    def get_count(polymer, steps_):
        if steps_ == 0:
            return Counter(polymer[1:])
        else:
            return sum((get_count(a + rules[a+b] + b, steps_ - 1)
                        for a, b in zip(polymer, polymer[1:])), start=Counter())

    count = get_count(template, steps)
    count[template[0]] += 1
    return max(count.values()) - min(count.values())


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
