from collections import defaultdict
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip().split()
            data.append(value)
    return data


@timeit
def part_1(data, default_registers=None):

    program = data
    registers = defaultdict(int)
    if default_registers is not None:
        registers.update(default_registers)
    instruction_pointer = 0

    while 0 <= instruction_pointer < len(program):

        instruction, *values = program[instruction_pointer]

        if instruction == 'cpy':
            x, y = values
            try:
                x = int(x)
            except ValueError:
                x = registers[x]
            registers[y] = x

        elif instruction == 'inc':
            x = values[0]
            registers[x] += 1

        elif instruction == 'dec':
            x = values[0]
            registers[x] -= 1

        elif instruction == 'jnz':
            x, y = values
            try:
                x = int(x)
            except ValueError:
                x = registers[x]
            if x != 0:
                try:
                    y = int(y)
                except ValueError:
                    y = registers[y]
                instruction_pointer += y - 1
        else:
            raise ValueError(f"Unknown instruction {(instruction, *values)} line {instruction_pointer}.")

        instruction_pointer += 1

    return registers['a']


@timeit
def part_2(data):
    return part_1.func(data, {'c': 1})


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
