
from collections import Counter


def solve(input_file):
    polymer = input_file.readline().strip()
    unit_types = set(unit.lower() for unit in polymer)

    best = len(polymer)
    for unit_type in unit_types:
        polymer_ = polymer.replace(unit_type, '').replace(unit_type.upper(), '')
        polymer_ = reduce(polymer_)
        if len(polymer_) < best:
            best = len(polymer_)

    return best


def reduce(polymer):
    i = 0
    while i + 1 < len(polymer):
        if polymer[i].lower() == polymer[i+1].lower() and polymer[i] != polymer[i+1]:
            polymer = polymer[:i] + polymer[i+2:]
            if i > 0:
                i -= 1
        else:
            i += 1
    return polymer


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
