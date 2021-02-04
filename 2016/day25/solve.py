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


def execute(program, default_registers=None):

    # Do not modify the original program
    program = list(tuple(instruction) for instruction in program)

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
        elif instruction == 'tgl':
            x = values[0]
            try:
                x = int(x)
            except ValueError:
                x = registers[x]

            if 0 <= instruction_pointer + x < len(program):
                instruction_, *values_ = program[instruction_pointer + x]
                if instruction_ in ('inc', 'dec', 'tgl'):
                    instruction_ = 'dec' if instruction_ == 'inc' else 'inc'
                elif instruction_ in ('cpy', 'jnz'):
                    instruction_ = 'cpy' if instruction_ == 'jnz' else 'jnz'

                program[instruction_pointer + x] = (instruction_, *values_)

        elif instruction == 'mul':
            x, y, z = values
            try:
                x = int(x)
            except ValueError:
                x = registers[x]
            try:
                y = int(y)
            except ValueError:
                y = registers[y]
            registers[z] += x*y

        elif instruction == 'out':
            x = values[0]
            try:
                x = int(x)
            except ValueError:
                x = registers[x]
            yield x

        else:
            raise ValueError(f"Unknown instruction {(instruction, *values)} line {instruction_pointer}.")

        instruction_pointer += 1

    return registers


@timeit
def part_1(data):
    a = 0
    while True:
        print()
        print(a)
        prev = 1
        for out in execute(program=data, default_registers={'a': a}):
            print(out, end='')
            if out != 1-prev:
                break
            prev = 1-prev
        a += 1


def main():
    data = get_data()
    part_1(data)


if __name__ == "__main__":
    main()
