from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            data.append(int(line))
    return data


@timeit
def part_1(data):

    program = data.copy()
    instruction = 0
    nb_steps = 0
    while 0 <= instruction < len(program):
        program[instruction] += 1
        instruction += program[instruction] - 1
        nb_steps += 1

    return nb_steps


@timeit
def part_2(data):

    program = data.copy()
    instruction = 0
    nb_steps = 0
    while 0 <= instruction < len(program):
        jump = program[instruction]
        if jump >= 3:
            program[instruction] -= 1
        else:
            program[instruction] += 1
        instruction += jump
        nb_steps += 1

    return nb_steps


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
