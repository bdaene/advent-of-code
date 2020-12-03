def execute(program, registers):
    bound_register = None

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

    op_funcs = {func.__name__: func for func in (addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti,
                                                 gtir, gtri, gtrr, eqir, eqri, eqrr)}

    # Compile
    commands = []
    for line in program:
        if line.startswith('#'):
            if line.startswith('#ip'):
                bound_register = int(line[3:])
        else:
            op_code, a, b, c = line.split()
            commands.append((op_funcs[op_code], int(a), int(b), int(c)))

    # Execute
    ip = 0
    while 0 <= ip < len(commands):
        if bound_register is not None:
            registers[bound_register] = ip
        op, a, b, c = commands[ip]
        op(a, b, c)
        if bound_register is not None:
            ip = registers[bound_register]
        ip += 1

    return registers


# The given program build a number then calculate the sum of the divisors of this number
def main():
    with open('input.txt') as input_file:
        program = [line for line in input_file]

    registers = execute(program, [0] * 6)
    print(registers[0])

    registers = execute(program, [1] + [0] * 5)
    print(registers[0])


if __name__ == "__main__":
    main()
