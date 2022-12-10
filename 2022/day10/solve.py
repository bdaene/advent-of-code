from itertools import islice

from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.split()
            data.append(tuple(value))
    return tuple(data)


def execute(program):
    clock, x = 0, 1

    for line in program:
        if line[0] == 'addx':
            v = int(line[1])
            clock += 1
            yield clock, x
            clock += 1
            yield clock, x
            x += v
        elif line[0] == 'noop':
            clock += 1
            yield clock, x


@timeit
def part_1(data):
    total = 0
    for clock, x in islice(execute(data), 19, None, 40):
        print(clock, x)
        total += clock * x
    return total


@timeit
def part_2(data):
    line = ""
    for clock, x in execute(data):
        line += '#' if -1 <= len(line)-x <= 1 else '.'
        if len(line) == 40:
            print(line)
            line = ""


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
