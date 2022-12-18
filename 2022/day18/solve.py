from itertools import product

import numpy
from matplotlib import pyplot
from utils import timeit


@timeit
def get_data():
    lava = set()
    with open('input.txt') as input_file:
        for line in input_file:
            x, y, z = map(int, line.strip().split(','))
            lava.add((x, y, z))
    return lava


def get_neighbors(x, y, z):
    return (x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)


@timeit
def part_1(lava):
    covered_faces = sum(other in lava for cube in lava for other in get_neighbors(*cube))
    return len(lava) * 6 - covered_faces


def flood_fill(lava, cube, limits):
    min_corner, max_corner = limits
    seen = {cube}
    stack = [cube]
    trapped = True
    while stack:
        cube = stack.pop()
        for other in get_neighbors(*cube):
            if other in lava:
                continue
            if other in seen:
                continue
            if not all(min_x <= other_x <= max_x for min_x, other_x, max_x in zip(min_corner, other, max_corner)):
                trapped = False
                continue
            seen.add(other)
            stack.append(other)

    return seen, trapped


def get_limits(cubes):
    min_corner = tuple(min(cube[x] for cube in cubes) for x in range(3))
    max_corner = tuple(max(cube[x] for cube in cubes) for x in range(3))
    return min_corner, max_corner


def get_trapped_cubes(lava):
    limits = get_limits(lava)
    min_corner, max_corner = limits

    trapped_cubes = set()
    outside_cubes = set()
    for cube in product(*(range(min_x, max_x + 1) for min_x, max_x in zip(min_corner, max_corner))):
        if cube in lava or cube in outside_cubes or cube in trapped_cubes:
            continue
        cubes, trapped = flood_fill(lava, cube, limits)
        if trapped:
            trapped_cubes |= cubes
        else:
            outside_cubes |= cubes

    return trapped_cubes


@timeit
def part_2(lava):
    trapped_cubes = get_trapped_cubes(lava)
    return part_1.func(lava) - part_1.func(trapped_cubes)


def get_numpy_volume(cubes, limits):
    min_corner, max_corner = limits
    volume = numpy.full(tuple(max_x - min_x + 1 for min_x, max_x in zip(min_corner, max_corner)), False)
    for cube in cubes:
        volume[tuple(cube_x - min_x for cube_x, min_x in zip(cube, min_corner))] = True
    return volume


def show(lava):
    limits = get_limits(lava)
    trapped_cubes = get_trapped_cubes(lava)

    axes = pyplot.figure().add_subplot(projection='3d')
    axes.voxels(get_numpy_volume(lava, limits), facecolors='#FF2807C0')
    axes.voxels(get_numpy_volume(trapped_cubes, limits), facecolors='#0059FFFF')
    pyplot.show()


def main():
    lava = get_data()
    part_1(lava)
    part_2(lava)
    show(lava)


if __name__ == "__main__":
    main()
