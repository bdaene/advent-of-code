import numpy
import re
from utils import timeit


@timeit
def get_data():
    data = []
    rect_pattern = re.compile(r'rect (\d+)x(\d+)')
    rotate_pattern = re.compile(r'rotate (?:row|column) ([xy])=(\d+) by (\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            if match := rect_pattern.match(line):
                width, height = match.groups()
                data.append(('rect', int(width), int(height)))
            elif match := rotate_pattern.match(line):
                direction, index, value = match.groups()
                data.append((f"rotate {direction}", int(index), int(value)))
            else:
                raise ValueError(f"Unmatched line: '{line}'")
    return data


def apply(screen, instructions):
    for instruction, *values in instructions:
        if instruction == 'rect':
            w, h = values
            screen[:w, :h] = '#'
        elif instruction == 'rotate y':
            y, shift = values
            screen[:, y] = numpy.roll(screen[:, y], shift)
        elif instruction == 'rotate x':
            x, shift = values
            screen[x, :] = numpy.roll(screen[x, :], shift)
        else:
            raise RuntimeError(f"Unknown instruction: {instruction}.")


def show(screen):
    print('\n'.join(''.join(screen[x, y] for x in range(screen.shape[0])) for y in range(screen.shape[1])))


@timeit
def part_1(data, width=50, height=6):

    screen = numpy.full((width, height), ' ')
    apply(screen, data)
    return (screen == '#').sum()


@timeit
def part_2(data, width=50, height=6):
    screen = numpy.full((width, height), ' ')
    apply(screen, data)
    show(screen)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
