import re

import numpy
from matplotlib import pyplot
from utils import timeit


@timeit
def get_instructions():
    instructions = []
    pattern = re.compile((r'([^\d]+) (\d+),(\d+) through (\d+),(\d+)'))
    with open('input.txt') as input_file:
        for line in input_file:
            action, *coordinates = pattern.match(line).groups()
            instructions.append((action, tuple(map(int, coordinates))))
    return instructions


@timeit
def part_1(instructions):
    lights = numpy.full((1000, 1000), False)

    for action, (a, b, c, d) in instructions:
        if action == 'turn off':
            lights[a:c + 1, b:d + 1] = False
        elif action == 'turn on':
            lights[a:c + 1, b:d + 1] = True
        else:
            lights[a:c + 1, b:d + 1] ^= True

    return lights.sum()


@timeit
def part_2(instructions):
    lights = numpy.full((1000, 1000), 0)

    for action, (a, b, c, d) in instructions:
        if action == 'turn off':
            lights[a:c + 1, b:d + 1] -= lights[a:c + 1, b:d + 1] > 0
        elif action == 'turn on':
            lights[a:c + 1, b:d + 1] += 1
        else:
            lights[a:c + 1, b:d + 1] += 2

    pyplot.imshow(lights)
    pyplot.show()
    return lights.sum()


def main():
    instructions = get_instructions()
    part_1(instructions)
    part_2(instructions)


if __name__ == "__main__":
    main()
