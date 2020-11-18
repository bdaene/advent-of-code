

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
                      99: 0}


def execute(program):

    def get_value(value, flag):
        if flag == 1:
            return value
        return program[value]

    instruction_pointer = 0
    while True:
        flags_, op = divmod(program[instruction_pointer], 100)
        instruction_pointer += 1

        values, flags = [], []
        for i in range(NUMBER_OF_OPERANDS[op]):
            value = program[instruction_pointer]
            values.append(value)
            flags_, flag = divmod(flags_, 10)
            flags.append(flag)
            instruction_pointer += 1

        if op == 1:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = get_value(a, fa) + get_value(b, fb)
        elif op == 2:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = get_value(a, fa) * get_value(b, fb)
        elif op == 3:
            (a,) = values
            program[a] = int(input("Need input: "))
        elif op == 4:
            (a,) = values
            (fa,) = flags
            print(get_value(a, fa))
        elif op == 5:
            a, b = values
            fa, fb = flags
            if get_value(a, fa) != 0:
                instruction_pointer = get_value(b, fb)
        elif op == 6:
            a, b = values
            fa, fb = flags
            if get_value(a, fa) == 0:
                instruction_pointer = get_value(b, fb)
        elif op == 7:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = 1 if (get_value(a, fa) < get_value(b, fb)) else 0
        elif op == 8:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = 1 if (get_value(a, fa) == get_value(b, fb)) else 0
        elif op == 99:
            return
        else:
            raise RuntimeError("Something went wrong")


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        solve(input_file)