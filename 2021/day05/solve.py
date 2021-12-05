from utils import timeit
import re
import numpy


@timeit
def get_data():
    data = []
    pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            x0, y0, x1, y1 = map(int, pattern.match(line).groups())
            data.append(((x0, y0), (x1, y1)))
    return tuple(data)


@timeit
def part_1(data):
    x_max, y_max = 0, 0
    for (x0, y0), (x1, y1) in data:
        x_max = max(x_max, x0, x1)
        y_max = max(y_max, y0, y1)

    grid = numpy.full((x_max+1, y_max+1), 0)
    for (x0, y0), (x1, y1) in data:
        (x0, y0), (x1, y1) = sorted(((x0, y0), (x1, y1)))
        if x0 == x1:
            y0, y1 = sorted((y0, y1))
            grid[x0, y0:y1+1] += 1
        if y0 == y1:
            grid[x0:x1+1, y0] += 1

    return (grid >= 2).sum()


@timeit
def part_2(data):
    x_max, y_max = 0, 0
    for (x0, y0), (x1, y1) in data:
        x_max = max(x_max, x0, x1)
        y_max = max(y_max, y0, y1)

    grid = numpy.full((x_max+1, y_max+1), 0)
    for (x0, y0), (x1, y1) in data:
        (x0, y0), (x1, y1) = sorted(((x0, y0), (x1, y1)))
        if x0 == x1:
            y0, y1 = sorted((y0, y1))
            grid[x0, y0:y1+1] += 1
        if y0 == y1:
            grid[x0:x1+1, y0] += 1
        if x1-x0 == y1-y0:
            for x in range(x0, x1+1):
                y = y0 + x - x0
                grid[x, y] += 1
        if x1-x0 == y0-y1:
            for x in range(x0, x1+1):
                y = y0 - (x - x0)
                grid[x, y] += 1

    return (grid >= 2).sum()


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
