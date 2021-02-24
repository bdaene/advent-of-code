from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


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
        if ip == 28:
            yield registers[a]
        op(a, b, c)
        if bound_register is not None:
            ip = registers[bound_register]
        ip += 1

    return registers


@timeit
def part_1(data):
    return next(execute(data, {0: None}))


@timeit
def part_2(data):
    seen = set()
    prev = None
    for value in execute(data, {0: None}):
        print(value)
        if value in seen:
            return prev
        prev = value
        seen.add(value)


@timeit
def part_2_bis():

    def loop(d):
        e = d | 0x10000
        d = 10649702
        while True:
            d += e & 0xff
            d &= 0xffffff
            d *= 65899
            d &= 0xffffff
            if 0x100 > e:
                return d
            else:
                e >>= 8

    seen = set()
    value = loop(0)
    while True:
        new_value = loop(value)
        if new_value in seen:
            break
        value = new_value
        seen.add(value)

    return value


def main():
    data = get_data()
    part_1(data)
    part_2(data)
    part_2_bis()


if __name__ == "__main__":
    main()
