import re
from bisect import bisect_left

import numpy
from utils import timeit


@timeit
def get_data():
    pattern = re.compile(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            state, *cuboid = pattern.match(line).groups()
            data.append((state == 'on', tuple(map(int, cuboid))))
        return tuple(data)


@timeit
def part_1(data):
    space = numpy.full((101, 101, 101), False)
    for state, cuboid in data:
        x0, x1, y0, y1, z0, z1 = cuboid
        space[x0 + 50:x1 + 51, y0 + 50:y1 + 51, z0 + 50:z1 + 51] = state
    return space.sum()


@timeit
def part_2(data):
    xs, ys, zs = set(), set(), set()
    for state, cuboid in data:
        x0, x1, y0, y1, z0, z1 = cuboid
        xs.add(x0)
        xs.add(x1 + 1)
        ys.add(y0)
        ys.add(y1 + 1)
        zs.add(z0)
        zs.add(z1 + 1)

    xs = tuple(sorted(xs))
    ys = tuple(sorted(ys))
    zs = tuple(sorted(zs))

    print(len(xs)-1, len(ys)-1, len(zs)-1, (len(xs)-1)*(len(ys)-1)*(len(zs)-1))

    space = numpy.full((len(xs) - 1, len(ys) - 1, len(zs) - 1), False)
    for state, cuboid in data:
        x0, x1, y0, y1, z0, z1 = cuboid
        x0 = bisect_left(xs, x0)
        x1 = bisect_left(xs, x1 + 1)
        y0 = bisect_left(ys, y0)
        y1 = bisect_left(ys, y1 + 1)
        z0 = bisect_left(zs, z0)
        z1 = bisect_left(zs, z1 + 1)
        space[x0:x1, y0:y1, z0:z1] = state

    total = 0
    for x, y, z in zip(*numpy.where(space)):
        total += (xs[x + 1] - xs[x]) * (ys[y + 1] - ys[y]) * (zs[z + 1] - zs[z])

    return total


def get_intersection(cuboid_a, cuboid_b):
    ax0, ax1, ay0, ay1, az0, az1 = cuboid_a
    bx0, bx1, by0, by1, bz0, bz1 = cuboid_b
    if ax0 > bx1 or ax1 < bx0 or ay0 > by1 or ay1 < by0 or az0 > bz1 or az1 < bz0:
        return None

    ix0, iy0, iz0 = max(ax0, bx0), max(ay0, by0), max(az0, bz0)
    ix1, iy1, iz1 = min(ax1, bx1), min(ay1, by1), min(az1, bz1)
    return ix0, ix1, iy0, iy1, iz0, iz1


def get_subtraction(cuboid_a, cuboid_b):
    intersection = get_intersection(cuboid_a, cuboid_b)
    if intersection is None:
        return cuboid_a,

    ax0, ax1, ay0, ay1, az0, az1 = cuboid_a
    bx0, bx1, by0, by1, bz0, bz1 = intersection

    cuboids = []
    if bx0 > ax0:
        cuboids.append((ax0, bx0 - 1, ay0, ay1, az0, az1))
    if bx1 < ax1:
        cuboids.append((bx1 + 1, ax1, ay0, ay1, az0, az1))
    if by0 > ay0:
        cuboids.append((bx0, bx1, ay0, by0 - 1, az0, az1))
    if by1 < ay1:
        cuboids.append((bx0, bx1, by1 + 1, ay1, az0, az1))
    if bz0 > az0:
        cuboids.append((bx0, bx1, by0, by1, az0, bz0 - 1))
    if bz1 < az1:
        cuboids.append((bx0, bx1, by0, by1, bz1 + 1, az1))
    return cuboids


@timeit
def part_2_bis(data):
    on_cuboids = []
    for state, cuboid in data:
        if state:
            cuboids = [cuboid]
            for on_cuboid in on_cuboids:
                cuboids = [sub_cuboid for cuboid in cuboids for sub_cuboid in get_subtraction(cuboid, on_cuboid)]
            on_cuboids += cuboids
        else:
            on_cuboids = [sub_cuboid for on_cuboid in on_cuboids for sub_cuboid in get_subtraction(on_cuboid, cuboid)]

    return sum((1 - x0 + x1) * (1 - y0 + y1) * (1 - z0 + z1) for x0, x1, y0, y1, z0, z1 in on_cuboids)


@timeit
def part_2_ter(data):
    cubes = set()

    for state, cuboid in data:
        x0, x1, y0, y1, z0, z1 = cuboid

        new_cubes = set()
        removed_cubes = set()
        for cube in cubes:
            c_x0, c_x1, c_y0, c_y1, c_z0, c_z1 = cube
            if c_x0 > x1 or c_x1 < x0 or c_y0 > y1 or c_y1 < y0 or c_z0 > z1 or c_z1 < z0:
                continue    # No intersection

            removed_cubes.add(cube)
            i_x0, i_x1 = max(x0, c_x0), min(x1, c_x1)
            i_y0, i_y1 = max(y0, c_y0), min(y1, c_y1)
            i_z0, i_z1 = max(z0, c_z0), min(z1, c_z1)

            if c_x0 < i_x0:
                new_cubes.add((c_x0, i_x0 - 1, c_y0, c_y1, c_z0, c_z1))
            if i_x1 < c_x1:
                new_cubes.add((i_x1 + 1, c_x1, c_y0, c_y1, c_z0, c_z1))
            if c_y0 < i_y0:
                new_cubes.add((i_x0, i_x1, c_y0, i_y0 - 1, c_z0, c_z1))
            if i_y1 < c_y1:
                new_cubes.add((i_x0, i_x1, i_y1 + 1, c_y1, c_z0, c_z1))
            if c_z0 < i_z0:
                new_cubes.add((i_x0, i_x1, i_y0, i_y1, c_z0, i_z0 - 1))
            if i_z1 < c_z1:
                new_cubes.add((i_x0, i_x1, i_y0, i_y1, i_z1 + 1, c_z1))

        cubes -= removed_cubes
        cubes |= new_cubes
        if state:
            cubes.add(cuboid)

    return sum((1 - x0 + x1) * (1 - y0 + y1) * (1 - z0 + z1) for x0, x1, y0, y1, z0, z1 in cubes)


def main():
    data = get_data()
    part_1(data)
    # part_2(data)    # Execution of part_2 took 148544.848ms. Result: 1294137045134837
    # part_2_bis(data)
    part_2_ter(data)


if __name__ == "__main__":
    main()
