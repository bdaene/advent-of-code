
import re


def solve(samples, progam):

    registers = [0] * 4

    def addr(a, b, c):
        registers[c] = registers[a] + registers[b]

    def addi(a, b, c):
        registers[c] = registers[a] + b

    def mulr(a, b, c):
        registers[c] = registers[a] * registers[b]

    def muli(a, b, c):
        registers[c] = registers[a] * b

    def banr(a, b, c):
        registers[c] = registers[a] & registers[b]

    def bani(a, b, c):
        registers[c] = registers[a] & b

    def borr(a, b, c):
        registers[c] = registers[a] | registers[b]

    def bori(a, b, c):
        registers[c] = registers[a] | b

    def setr(a, _, c):
        registers[c] = registers[a]

    def seti(a, _, c):
        registers[c] = a

    def gtir(a, b, c):
        registers[c] = 1 if a > registers[b] else 0

    def gtri(a, b, c):
        registers[c] = 1 if registers[a] > b else 0

    def gtrr(a, b, c):
        registers[c] = 1 if registers[a] > registers[b] else 0

    def eqir(a, b, c):
        registers[c] = 1 if a == registers[b] else 0

    def eqri(a, b, c):
        registers[c] = 1 if registers[a] == b else 0

    def eqrr(a, b, c):
        registers[c] = 1 if registers[a] == registers[b] else 0

    op_funcs = {addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr}

    def match(before, command, after, available_op_funcs):
        valid_op_funcs = set()
        for func in available_op_funcs:
            registers.clear()
            registers.extend(before)
            func(*command[1:])
            if tuple(registers) == after:
                valid_op_funcs.add(func)
        return valid_op_funcs

    count = 0
    for before, command, after in samples:
        print(before, command, after)
        valid_op_funcs = match(before, command, after, op_funcs)
        print(valid_op_funcs)
        if len(valid_op_funcs) >= 3:
            count += 1

    print(f"{count} samples behave like three or more opcodes")

    available_op_funcs = op_funcs.copy()
    available_op_codes = set(range(len(op_funcs)))
    possibles_op_funcs = {code: available_op_funcs.copy() for code in available_op_codes}
    op_codes = {}

    while len(available_op_funcs) > 0:
        for before, command, after in samples:
            op_code = command[0]
            if op_code not in available_op_codes:
                continue
            op_funcs = match(before, command, after, available_op_funcs)
            possibles_op_funcs[op_code] &= op_funcs

            assert(len(possibles_op_funcs[op_code]) > 0)

            if len(possibles_op_funcs[op_code]) == 1:
                func = possibles_op_funcs[op_code].pop()
                del possibles_op_funcs[op_code]

                available_op_codes.remove(op_code)
                available_op_funcs.remove(func)
                op_codes[op_code] = func

                for op_code in possibles_op_funcs:
                    possibles_op_funcs[op_code].discard(func)

        print(len(op_codes), op_codes)

    registers.clear()
    registers.extend([0]*4)

    for command in program:
        op_code = command[0]
        op_codes[op_code](*command[1:])

    return registers[0]


BEFORE_PATTERN = re.compile(r'Before: \[(.*)\]')
AFTER_PATTERN = re.compile(r'After: {2}\[(.*)\]')

if __name__ == "__main__":
    samples = []
    program = []
    with open('input.txt', 'r') as input_file:
        while True:
            line = input_file.readline().strip()
            if len(line) == 0:
                break
            before = tuple(map(int, BEFORE_PATTERN.match(line).group(1).split(',')))
            line = input_file.readline().strip()
            command = tuple(map(int, line.split(' ')))
            line = input_file.readline().strip()
            after = tuple(map(int, AFTER_PATTERN.match(line).group(1).split(',')))
#            print(before, command, after)
            samples.append((before, command, after))
            input_file.readline()

        input_file.readline()
        input_file.readline()

        while True:
            line = input_file.readline().strip()
            if len(line) == 0:
                break
            command = tuple(map(int, line.split(' ')))
#            print(command)
            program.append(command)

    print(solve(samples, command))
