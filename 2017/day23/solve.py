from collections import defaultdict, Counter
from utils import timeit


@timeit
def get_data():

    def try_int(value):
        try:
            return int(value)
        except ValueError:
            return value

    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            operation = tuple(map(try_int, line.split()))
            data.append(operation)
    return data


def execute(program, default_registers=None):

    registers = defaultdict(int)
    if default_registers is not None:
        registers.update(default_registers)

    def get_value(value):
        if isinstance(value, int):
            return value
        return registers[value]

    instruction_pointer = 0
    op_count = Counter()
    while 0 <= instruction_pointer < len(program):
        op, x, y = program[instruction_pointer]
        op_count[op] += 1
        if op == 'set':
            registers[x] = get_value(y)
        elif op == 'sub':
            registers[x] -= get_value(y)
        elif op == 'mul':
            registers[x] *= get_value(y)
        elif op == 'mod':
            registers[x] %= get_value(y)
        elif op == 'jnz':
            if get_value(x) != 0:
                instruction_pointer += get_value(y) - 1
        elif op == 'jgz':
            if get_value(x) > 0:
                instruction_pointer += get_value(y) - 1
        else:
            raise ValueError(f"Unknown instruction: {op, x, y}.")

        instruction_pointer += 1

    return registers, op_count


@timeit
def part_1(data):
    registers, op_count = execute(data)
    return op_count['mul']


@timeit
def part_2(data):

    is_prime_routine = [
        ('set', 'f', 1),
        ('set', 'd', 2),

        ('set', 'g', 'b'),
        ('mod', 'g', 'd'),
        ('jnz', 'g', 3),
        ('set', 'f', 0),
        ('jnz', 1, 7),

        ('sub', 'd', -1),
        ('set', 'g', 'd'),
        ('mul', 'g', 'g'),
        ('sub', 'g', 'b'),
        ('jgz', 'g', 2),
        ('jnz', 1, -9),
    ]
    data = data[:8] + is_prime_routine + data[24:]
    data[-1] = ('jnz', 1, 9-len(data))

    registers, op_count = execute(data, {'a': 1})
    return registers['h']


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
