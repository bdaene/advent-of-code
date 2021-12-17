import math
import re

from utils import timeit


@timeit
def get_data():
    pattern = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')
    with open('input.txt') as input_file:
        x_min, x_max, y_min, y_max = map(int, pattern.match(input_file.readline()).groups())
    return x_min, x_max, y_min, y_max


def simulate_trajectory(vx, vy, target):
    x_min, x_max, y_min, y_max = target

    x, y = 0, 0
    trajectory = [(x, y)]
    while True:
        x += vx
        y += vy
        vx = max(vx - 1, 0)
        vy -= 1
        trajectory.append((x, y))

        if x_min <= x <= x_max and y_min <= y <= y_max:
            return trajectory

        if x > x_max or (y < y_min and vy < 0):
            return None


@timeit
def part_1(target):
    x_min, x_max, y_min, y_max = target

    best = 0
    for vy in range(1000):
        for vx in range(x_max + 1):
            trajectory = simulate_trajectory(vx, vy, target)
            if trajectory:
                y_max = max(y for x, y in trajectory)
                if y_max > best:
                    # print(trajectory)
                    best = y_max

    return best


@timeit
def part_2(target):
    x_min, x_max, y_min, y_max = target

    velocities = []
    for vy in range(-1000, 1000):
        for vx in range(x_max + 1):
            trajectory = simulate_trajectory(vx, vy, target)
            if trajectory:
                velocities.append((vx, vy))

    return len(velocities)


@timeit
def part_1_bis(target):
    x_min, x_max, y_min, y_max = target

    # y = t*vy - t*(t-1)/2
    # (y_min + t*(t-1)/2)/t <= vy <= (y_max + t*(t-1)/2)/t

    best = 0
    for t in range(1, 1000):
        vy_min = math.ceil((y_min + t * (t - 1) // 2) / t)
        vy_max = math.floor((y_max + t * (t - 1) // 2) / t)

        if -vy_min-1 < y_min:
            break

        if vy_max >= 0 and vy_min <= vy_max:
            best = max(best, vy_max * (vy_max + 1) // 2)

    return best


@timeit
def part_2_bis(target):
    x_min, x_max, y_min, y_max = target

    # y = t*vy - t*(t-1)/2
    # (y_min + t*(t-1)/2)/t <= vy <= (y_max + t*(t-1)/2)/t

    # x = t*vx - t*(t-1)/2 if t < vx else vx*(vx-1)/2
    # (x_min + t*(t-1)/2)/t <= vx <= (x_max + t*(t-1)/2)/t if t <= vx
    # ((8*x_min+1)**.5-1)/2 <= vx <= ((8*x_max+1)**.5-1)/2 it t >= vx

    vx_min_limit = math.ceil(((8 * x_min + 1) ** .5 - 1) / 2)
    vx_max_limit = math.floor(((8 * x_max + 1) ** .5 - 1) / 2)

    velocities = set()
    for t in range(1, 1000):
        vy_min = math.ceil((y_min + t * (t - 1) // 2) / t)
        vy_max = math.floor((y_max + t * (t - 1) // 2) / t)

        if -vy_min-1 < y_min:
            break

        vx_min = math.ceil((x_min + t * (t - 1) // 2) / t)
        vx_max = math.floor((x_max + t * (t - 1) // 2) / t)
        if vx_min <= t:
            vx_min = vx_min_limit
        if vx_max <= t:
            vx_max = vx_max_limit

        for vx in range(vx_min, vx_max + 1):
            for vy in range(vy_min, vy_max + 1):
                velocities.add((vx, vy))

    return len(velocities)


@timeit
def part_1_ter(target):
    x_min, x_max, y_min, y_max = target

    # y positions are symmetric around maximum height. So maximum vy is when -(vy+1) is in target.
    vy_max = -y_min - 1
    return vy_max * (vy_max + 1) // 2


def main():
    data = get_data()
    # part_1(data)
    # part_2(data)
    part_1_bis(data)
    part_1_ter(data)
    part_2_bis(data)


if __name__ == "__main__":
    main()
