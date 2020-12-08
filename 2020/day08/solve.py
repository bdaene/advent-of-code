def execute(program):
    executed = set()
    accumulator = 0
    ip = 0
    while ip < len(program) and ip not in executed:
        executed.add(ip)
        op, value = program[ip]
        if op == 'acc':
            accumulator += value
        elif op == 'jmp':
            ip += value - 1
        elif op == 'nop':
            pass  # No operation
        else:
            raise NotImplementedError(f"Unknown operation {op} {value}.")

        ip += 1

    return accumulator, ip


def part_1(program):
    accumulator, _ = execute(program)
    print(accumulator)


def part_2(program):
    for ip, (op, value) in enumerate(program):
        if op == 'acc':
            continue
        else:
            instruction = program[ip]
            program[ip] = ('nop' if op == 'jmp' else 'jmp', value)
            accumulator, ip_ = execute(program)
            if ip_ >= len(program):
                print(accumulator)
            program[ip] = instruction


def get_program(input_file):
    program = []
    for line in input_file:
        op, value = line.split()
        program.append((op, int(value)))
    return program


def main():
    with open('input.txt') as input_file:
        program = get_program(input_file)

    print(program)
    part_1(program)
    part_2(program)


if __name__ == "__main__":
    main()
