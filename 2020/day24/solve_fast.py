from collections import defaultdict, Counter

import numpy
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
        u, v = 0, 0
        for direction in instruction:
            du, dv = directions[direction]
            u += du
            v += dv
        black_tiles[(u, v)] ^= True
    return black_tiles


@timeit
def part_1(instructions):
    black_tiles = apply(instructions)
    return Counter(black_tiles.values())[True]


@timeit
def part_2(instructions, nb_days=100):
    black_tiles = apply(instructions)

    min_u, max_u, min_v, max_v = 0, 0, 0, 0
    for u, v in black_tiles:
        min_u = min(min_u, u)
        max_u = max(max_u, u)
        min_v = min(min_v, v)
        max_v = max(max_v, v)

    tiles = numpy.full((max_u - min_u + 1, max_v - min_v + 1), False)
    for (u, v), black in black_tiles.items():
        tiles[u - min_u, v - min_v] = black

    for _ in range(nb_days):
        count = numpy.zeros((tiles.shape[0] + 2, tiles.shape[1] + 2), dtype=int)
        count[:-2, 1:-1] += tiles
        count[2:, 1:-1] += tiles
        count[1:-1, :-2] += tiles
        count[1:-1, 2:] += tiles
        count[2:, :-2] += tiles
        count[:-2, 2:] += tiles

        tiles_ = (count == 2)
        tiles_[1:-1, 1:-1] |= tiles & (count[1:-1, 1:-1] == 1)
        tiles = tiles_

    return tiles.sum()


def main():
    instructions = get_instructions()
    part_1(instructions)
    part_2(instructions)


if __name__ == "__main__":
    main()
