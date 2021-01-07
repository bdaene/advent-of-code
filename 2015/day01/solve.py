from utils import timeit


@timeit
def get_instructions():
    with open('input.txt') as input_file:
        return input_file.readline().strip()


@timeit
def part_1(instructions):
    floor = 0
    for c in instructions:
        floor += 1 if c == '(' else -1
    return floor


@timeit
def part_2(instructions):
    floor = 0
    for i, c in enumerate(instructions, 1):
        floor += 1 if c == '(' else -1
        if floor < 0:
            return i


def main():
    instructions = get_instructions()
    part_1(instructions)
    part_2(instructions)


if __name__ == "__main__":
    main()
