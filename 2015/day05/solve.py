import re
from collections import Counter

from utils import timeit


@timeit
def get_strings():
    strings = []
    with open('input.txt') as input_file:
        for line in input_file:
            strings.append(line.strip())
    return strings


@timeit
def part_1(strings):
    nice = 0
    for string in strings:
        count = Counter(string)
        if not sum(count[c] for c in 'aeiou') >= 3:
            continue
        if not any(a == b for a, b in zip(string, string[1:])):
            continue
        if any(s in string for s in ('ab', 'cd', 'pq', 'xy')):
            continue

        nice += 1

    return nice


@timeit
def part_2(strings):
    rule1 = re.compile(r'(\w{2}).*\1')
    rule2 = re.compile(r'(\w)\w\1')

    return sum(1 for string in strings if rule1.search(string) and rule2.search(string))


def main():
    strings = get_strings()
    part_1(strings)
    part_2(strings)


if __name__ == "__main__":
    main()
