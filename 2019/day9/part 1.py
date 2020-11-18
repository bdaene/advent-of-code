

from collections import defaultdict


def solve(input_file):
    program = list(map(int, input_file.readline().split(',')))
    execute(program)


"""
Operations :
    1 a b c     add             a + b -> c
    2 a b c     multiply        a * b -> c
    3 a         input           input -> a
    4 a         output          a -> output
    5 a b       jump-if-true    (a != 0) => b -> instruction pointer
    6 a b       jump-if-false   (a == 0) => b -> instruction pointer
    7 a b c     less than       (a < b) -> c
    8 a b c     equals          (a == b) -> c
    9 a         change base     relative_base += a
   99           halt
"""
NUMBER_OF_OPERANDS = {1: 3,
                      2: 3,
                      3: 1,
                      4: 1,
                      5: 2,
                      6: 2,
                      7: 3,
                      8: 3,
                      9: 1,
                      99: 0}


def default_input():
    return int(input("Need input: "))


def execute(program_, input_func=default_input, output_func=print):

    program = defaultdict(int)
    for index, value in enumerate(program_):
        program[index] = value

    relative_base = 0

    def get_value(flag_, index_):
        if flag_ == 0:
            return program[index_]
        elif flag_ == 1:
            return index_
        elif flag_ == 2:
            return program[relative_base + index_]
        else:
            raise RuntimeError(f"Unknown flag {flag_} in get_value({flag_}, {index_})")

    def set_value(flag_, index_, value_):
        if flag_ == 0:
            program[index_] = value_
        elif flag_ == 1:
            raise RuntimeError(f"Cannot set to value in set_value({flag_}, {index_}, {value_})")
        elif flag_ == 2:
            program[relative_base + index_] = value_
        else:
            raise RuntimeError(f"Unknown flag {flag_} in set_value({flag_}, {index_}, {value_})")

    instruction_pointer = 0
    while True:
        flags_, op = divmod(program[instruction_pointer], 100)
        instruction_pointer += 1

        values, flags = [], []
        for i in range(NUMBER_OF_OPERANDS[op]):
            values.append(program[instruction_pointer])
            flags_, flag = divmod(flags_, 10)
            flags.append(flag)
            instruction_pointer += 1

        if op == 1:
            a, b, c = values
            fa, fb, fc = flags
            set_value(fc, c, get_value(fa, a) + get_value(fb, b))
        elif op == 2:
            a, b, c = values
            fa, fb, fc = flags
            set_value(fc, c, get_value(fa, a) * get_value(fb, b))
        elif op == 3:
            (a,) = values
            (fa,) = flags
            set_value(fa, a, input_func())
        elif op == 4:
            (a,) = values
            (fa,) = flags
            output_func(get_value(fa, a))
        elif op == 5:
            a, b = values
            fa, fb = flags
            if get_value(fa, a) != 0:
                instruction_pointer = get_value(fb, b)
        elif op == 6:
            a, b = values
            fa, fb = flags
            if get_value(fa, a) == 0:
                instruction_pointer = get_value(fb, b)
        elif op == 7:
            a, b, c = values
            fa, fb, fc = flags
            set_value(fc, c, 1 if (get_value(fa, a) < get_value(fb, b)) else 0)
        elif op == 8:
            a, b, c = values
            fa, fb, fc = flags
            set_value(fc, c, 1 if (get_value(fa, a) == get_value(fb, b)) else 0)
        elif op == 9:
            (a,) = values
            (fa,) = flags
            relative_base += get_value(fa, a)
        elif op == 99:
            return
        else:
            raise RuntimeError("Something went wrong")


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))