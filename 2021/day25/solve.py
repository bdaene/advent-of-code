import numpy
from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(tuple(line.strip()) for line in input_file)


@timeit
def part_1(data):
    floor = numpy.array(data)

    step, moving = 0, True
    while moving:
        step += 1
        # Move east
        right = numpy.roll(floor, -1, axis=1)
        free = (floor == '>') & (right == '.')
        moving = free.any()
        floor[free] = '.'
        floor[numpy.roll(free, 1, axis=1)] = '>'
        # Move south
        down = numpy.roll(floor, -1, axis=0)
        free = (floor == 'v') & (down == '.')
        moving |= free.any()
        floor[free] = '.'
        floor[numpy.roll(free, 1, axis=0)] = 'v'

    return step


@timeit
def part_2(data):
    return len(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
