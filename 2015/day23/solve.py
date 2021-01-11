from collections import defaultdict

from utils import timeit


@timeit
def get_program():
    program = []
    with open('input.txt') as input_file:
        for line in input_file:
            op, values = line[:3], line[4:]
            values = values.strip().split(',')
            values_ = []
            for v in values:
                try:
                    values_.append(int(v))
                except ValueError:
                    values_.append(v)
            program.append((op,) + tuple(values_))
    return tuple(program)


@timeit
def part_1(program, set_registers=None):
    registers = defaultdict(int)
    if set_registers is not None:
        registers.update(set_registers)

    instruction_pointer = 0

    while 0 <= instruction_pointer < len(program):

        op, *values = program[instruction_pointer]

        a = values[0]
        if op == 'hlf':
            registers[a] //= 2
        elif op == 'tpl':
            registers[a] *= 3
        elif op == 'inc':
            registers[a] += 1
        elif op == 'jmp':
            instruction_pointer += a - 1
        elif op == 'jie':
            b = values[1]
            if registers[a] & 1 == 0:
                instruction_pointer += b - 1
        elif op == 'jio':
            b = values[1]
            if registers[a] == 1:
                instruction_pointer += b - 1
        else:
            raise ValueError(f"Unknown instruction {op} at line {instruction_pointer}.")

        instruction_pointer += 1

    return registers['b']


@timeit
def part_2(program):
    return part_1.func(program, {'a': 1})


def main():
    program = get_program()
    part_1(program)
    part_2(program)


if __name__ == "__main__":
    main()
