

def solve(input_file):
    program = list(map(int, input_file.readline().split(',')))
    execute(program)


NUMBER_OF_OPERANDS = {1: 3, 2: 3, 3: 1, 4: 1, 99: 0}
"""
Operations :
    1 a b c     add         a b -> c
    2 a b c     multiply    a b -> c
    3 a         input           -> a
    4 a         output        a ->
   99           halt
"""


def execute(program):
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
            program[c] = (a if fa == 1 else program[a]) + (b if fb == 1 else program[b])
        elif op == 2:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = (a if fa == 1 else program[a]) * (b if fb == 1 else program[b])
        elif op == 3:
            (a,) = values
            program[a] = int(input("Need input: "))
        elif op == 4:
            (a,) = values
            (fa,) = flags
            print((a if fa == 1 else program[a]))
        elif op == 99:
            return
        else:
            raise RuntimeError("Something went wrong")


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        solve(input_file)