import re
from collections import Counter
from utils import timeit


@timeit
def get_data():
    data = {}
    pattern = re.compile(r'(\w+) \((\d+)\)(.*)')
    with open('input.txt') as input_file:
        for line in input_file:
            name, weight, other_programs = pattern.match(line).groups()
            if other_programs.startswith(' -> '):
                other_programs = set(other_programs[4:].split(', '))
            else:
                other_programs = set()
            data[name] = (int(weight), other_programs)
    return data


@timeit
def part_1(data):
    names = data.keys()
    for weight, programs in data.values():
        assert all(program in names for program in programs)
        names -= programs
    return names.pop()


@timeit
def part_2(data):
    total_weight = {}

    def get_total_weight(name):
        if name not in total_weight:
            program_weight, program_programs = data[name]
            total_weight[name] = program_weight + sum(map(get_total_weight, program_programs))
        return total_weight[name]

    names = data.keys()
    for weight, programs in data.values():
        assert all(program in names for program in programs)
        names -= programs
    root = names.pop()

    def is_balanced(name):
        program_weight, program_programs = data[name]
        return all(get_total_weight(sub_program) * len(program_programs) == get_total_weight(name) - program_weight
                   for sub_program in program_programs)

    next_root = root
    while next_root:
        root = next_root
        next_root = None
        for program in data[root][1]:
            if not is_balanced(program):
                next_root = program

    programs = data[root][1]
    weights = Counter(map(get_total_weight, programs))
    expected_weight = sorted(weights, key=weights.get)[-1]

    for program in programs:
        if get_total_weight(program) != expected_weight:
            return data[program][0] + expected_weight - get_total_weight(program)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
