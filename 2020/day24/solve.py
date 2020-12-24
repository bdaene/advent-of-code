from collections import defaultdict, Counter

import numpy
from array2gif import write_gif
from cmath import rect, pi
from utils import timeit


@timeit
def get_instructions():
    with open('input.txt') as input_file:
        instructions = []
        for line in input_file:
            i = 0
            instruction = []
            while i < len(line) and not line[i].isspace():
                if line[i] == 'n' or line[i] == 's':
                    instruction.append(line[i:i + 2])
                    i += 2
                else:
                    instruction.append(line[i])
                    i += 1
            instructions.append(tuple(instruction))
    return tuple(instructions)


directions = {'e': (1, 0),
              'se': (1, -1),
              'sw': (0, -1),
              'w': (-1, 0),
              'nw': (-1, 1),
              'ne': (0, 1)}


def apply(instructions):
    black_tiles = defaultdict(bool)
    for instruction in instructions:
        x, y = 0, 0
        for direction in instruction:
            dx, dy = directions[direction]
            x += dx
            y += dy
        black_tiles[(x, y)] ^= True
    return black_tiles


def get_array(black_tiles, size=512):
    dx = rect(1, 0)
    dy = rect(1, -pi / 3)
    coordinates = [x * dx + y * dy for (x, y), black in black_tiles.items() if black]
    x_max = max(abs(c.real) for c in coordinates)
    y_max = max(abs(c.imag) for c in coordinates)

    radius = size / 4 / (max(x_max, y_max) + 1)

    array = numpy.full((3, size, size), 255, dtype=numpy.uint8)
    for c in coordinates:
        c *= radius * 2
        for x in range(int(c.real - radius), int(c.real)):
            for y in range(int(c.imag - radius + (c.real - x) / 2) - 1,
                           int(c.imag + radius - (c.real - x) / 2) + 1):
                array[:, y + size // 2, x + size // 2] = (0, 0, 0)
        for x in range(int(c.real), int(c.real + radius) + 1):
            for y in range(int(c.imag - radius + (x - c.real) / 2) - 1,
                           int(c.imag + radius - (x - c.real) / 2) + 1):
                array[:, y + size // 2, x + size // 2] = (0, 0, 0)

    return array


@timeit
def part_1(instructions):
    black_tiles = apply(instructions)
    return Counter(black_tiles.values())[True]


@timeit
def part_2(instructions, nb_days=100):
    black_tiles = apply(instructions)
    images = []

    for _ in range(nb_days):
        counts = Counter()
        for (x, y), black in black_tiles.items():
            if black:
                for dx, dy in directions.values():
                    counts[x + dx, y + dy] += 1

        for tile in black_tiles.keys() | counts.keys():
            black, count = black_tiles[tile], counts[tile]
            if black and (count == 0 or count > 2):
                black_tiles[tile] = False
            elif not black and count == 2:
                black_tiles[tile] = True

        images.append(get_array(black_tiles))
        # print(Counter(black_tiles.values())[True])

    write_gif([images[0] * 10] + images + [images[-1]] * 10, 'day24.gif')
    return Counter(black_tiles.values())[True]


def main():
    instructions = get_instructions()
    part_1(instructions)
    part_2(instructions)


if __name__ == "__main__":
    main()
