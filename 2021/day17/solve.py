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
        for vx in range(x_max+1):
            trajectory = simulate_trajectory(vx, vy, target)
            if trajectory:
                y_max = max(y for x, y in trajectory)
                if y_max > best:
                    print(trajectory)
                    best = y_max

    return best


@timeit
def part_2(target):
    x_min, x_max, y_min, y_max = target

    velocities = []
    for vy in range(-1000, 1000):
        for vx in range(x_max+1):
            trajectory = simulate_trajectory(vx, vy, target)
            if trajectory:
                velocities.append((vx, vy))

    return len(velocities)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
