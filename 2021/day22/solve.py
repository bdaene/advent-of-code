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
    ix0, iy0, iz0 = max(ax0, bx0), max(ay0, by0), max(az0, bz0)
    ix1, iy1, iz1 = min(ax1, bx1), min(ay1, by1), min(az1, bz1)
    if ix0 <= ix1 and iy0 <= iy1 and iz0 <= iz1:
        return ix0, ix1, iy0, iy1, iz0, iz1
    else:
        return None


def get_subtraction(cuboid_a, cuboid_b):
    intersection = get_intersection(cuboid_a, cuboid_b)
    if intersection is None:
        return cuboid_a,

    ax0, ax1, ay0, ay1, az0, az1 = cuboid_a
    bx0, bx1, by0, by1, bz0, bz1 = intersection

    cuboids = []
    if bx0 > ax0:
        cuboids.append((ax0, bx0 - 1, ay0, ay1, az0, az1))
        ax0 = bx0
    if bx1 < ax1:
        cuboids.append((bx1 + 1, ax1, ay0, ay1, az0, az1))
        ax1 = bx1
    if by0 > ay0:
        cuboids.append((ax0, ax1, ay0, by0 - 1, az0, az1))
        ay0 = by0
    if by1 < ay1:
        cuboids.append((ax0, ax1, by1 + 1, ay1, az0, az1))
        ay1 = by1
    if bz0 > az0:
        cuboids.append((ax0, ax1, ay0, ay1, az0, bz0 - 1))
    if bz1 < az1:
        cuboids.append((ax0, ax1, ay0, ay1, bz1 + 1, az1))
    return cuboids


def get_total_volume(data):
    on_cuboids = []
    for state, cuboid in data:
        if state:
            cuboids = [cuboid]
            for on_cuboid in on_cuboids:
                cuboids = [sub_cuboid for cuboid in cuboids for sub_cuboid in get_subtraction(cuboid, on_cuboid)]
            on_cuboids += cuboids
        else:
            on_cuboids = [sub_cuboid for on_cuboid in on_cuboids for sub_cuboid in get_subtraction(on_cuboid, cuboid)]

    total = 0
    for cuboid in on_cuboids:
        x0, x1, y0, y1, z0, z1 = cuboid
        total += (1 - x0 + x1) * (1 - y0 + y1) * (1 - z0 + z1)

    return total


@timeit
def part_2_bis(data):
    return get_total_volume(data[:20]) + get_total_volume(data[20:])


def main():
    data = get_data()
    part_1(data)
    # part_2(data)    # Execution of part_2 took 148544.848ms. Result: 1294137045134837
    part_2_bis(data)


if __name__ == "__main__":
    main()
