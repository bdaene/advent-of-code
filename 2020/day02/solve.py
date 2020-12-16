import re
from collections import Counter

from utils import timeit


@timeit
def part_1(rules, passwords):
    count = 0
    for (a, b, c), password in zip(rules, passwords):
        if a <= Counter(password)[c] <= b:
            count += 1
    return count


@timeit
def part_2(rules, passwords):
    count = 0
    for (a, b, c), password in zip(rules, passwords):
        if (password[a - 1] == c) != (password[b - 1] == c):
            count += 1
    return count


def main():
    rules, passwords = [], []
    pattern = re.compile(r'^(\d+)-(\d+) (\w): (\w+)$')
    with open('input.txt') as input_file:
        for line in input_file:
            entry = re.match(pattern, line)
            a, b, c, p = entry.groups()
            rules.append((int(a), int(b), c))
            passwords.append(p)

    part_1(rules, passwords)
    part_2(rules, passwords)


if __name__ == "__main__":
    main()
