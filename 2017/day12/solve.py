import re
from utils import timeit


@timeit
def get_data():
    data = {}
    pattern = re.compile(r'(\d+) <-> (\d+(?:, \d+)*)')
    with open('input.txt') as input_file:
        for line in input_file:
            program, other_programs = pattern.match(line).groups()
            data[int(program)] = frozenset(map(int, other_programs.split(', ')))
    return data


@timeit
def part_1(data):

    seen = {0}
    stack = [0]
    while stack:
        program = stack.pop()
        for other_program in data[program]:
            if other_program not in seen:
                seen.add(other_program)
                stack.append(other_program)

    return len(seen)


@timeit
def part_2(data):

    parents = {}

    def merge(a, b):
        a_parent = get_parent(a)
        b_parent = get_parent(b)
        parents[a_parent] = b_parent

    def get_parent(a):
        if a not in parents:
            parents[a] = a
            return a
        path = []
        while parents[a] != a:
            path.append(a)
            a = parents[a]
        for b in path:
            parents[b] = a
        return a

    for program, other_programs in data.items():
        for other_program in other_programs:
            merge(program, other_program)

    for program in data:
        get_parent(program)

    return len(set(parents.values()))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
