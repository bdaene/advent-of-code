
def solve(input_file):
    program = list(map(int, input_file.readline().split(',')))
    program[1] = 12
    program[2] = 2

    execute(program)

    return program[0]


def execute(program):
    instruction_pointer = 0
    while True:
        if program[instruction_pointer] == 1:
            a, b, c = program[instruction_pointer+1:instruction_pointer+4]
            program[c] = program[a] + program[b]
            instruction_pointer += 4
        elif program[instruction_pointer] == 2:
            a, b, c = program[instruction_pointer+1:instruction_pointer+4]
            program[c] = program[a] * program[b]
            instruction_pointer += 4
        elif program[instruction_pointer] == 99:
            return
        else:
            raise RuntimeError("Something went wrong")


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))