import re
from collections import defaultdict
from utils import timeit


@timeit
def get_data():
    data = []
    pattern = re.compile(r'(\w+) (inc|dec) (-?\d+) if (\w+) (==|!=|<|>|<=|>=) (-?\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            register_a, operation, value_a, register_b, test, value_b = pattern.match(line).groups()
            data.append((register_a, operation, int(value_a), register_b, test, int(value_b)))
    return data


def apply_test(a, op, b):
    if op == '==':
        return a == b
    elif op == '!=':
        return a != b
    elif op == '<':
        return a < b
    elif op == '>':
        return a > b
    elif op == '<=':
        return a <= b
    elif op == '>=':
        return a >= b
    else:
        raise ValueError(f"Unknown op '{op}'.")


@timeit
def part_1(data):

    registers = defaultdict(int)
    for register_a, operation, value_a, register_b, test, value_b in data:
        if apply_test(registers[register_b], test, value_b):
            if operation == 'inc':
                registers[register_a] += value_a
            else:
                registers[register_a] -= value_a

    return max(registers.values())


@timeit
def part_2(data):

    registers = defaultdict(int)
    max_value = 0
    for register_a, operation, value_a, register_b, test, value_b in data:
        if apply_test(registers[register_b], test, value_b):
            if operation == 'inc':
                registers[register_a] += value_a
            else:
                registers[register_a] -= value_a
            max_value = max(max_value, registers[register_a])

    return max_value


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
