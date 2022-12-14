import numpy
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            points = tuple((int(x), int(y)) for x, y in (point.split(',') for point in line.strip().split(' -> ')))
            data.append(points)
    return data


def build_grid(paths, infinite_floor=False):
    paths.append(((500, 0),))
    min_x = min(point[0] for path in paths for point in path)
    min_y = min(point[1] for path in paths for point in path)
    max_x = max(point[0] for path in paths for point in path)
    max_y = max(point[1] for path in paths for point in path)

    if infinite_floor:
        max_y += 2
        min_x = min(min_x, 500 - (max_y - min_y) - 2)
        max_x = max(max_x, 500 + (max_y - min_y) + 2)
        paths = [((min_x, max_y), (max_x, max_y))] + paths

    paths = tuple(tuple((x - min_x, max_y - y) for x, y in path) for path in paths)
    start_point = paths[-1][0]

    grid = numpy.full((max_x - min_x + 1, max_y - min_y + 1), '.')
    for path in paths:
        for (a_x, a_y), (b_x, b_y) in zip(path, path[1:]):
            a_x, b_x = min(a_x, b_x), max(a_x, b_x)
            a_y, b_y = min(a_y, b_y), max(a_y, b_y)

            grid[a_x:b_x + 1, a_y:b_y + 1] = '#'

    return grid, start_point


def get_resting_place(path, grid):
    x, y = path[-1]
    while True:
        if not 0 <= x < grid.shape[0] or not 0 <= y < grid.shape[1]:
            return None
        y -= 1
        if grid[x][y] == '.':
            pass
        elif grid[x - 1][y] == '.':
            x -= 1
        elif grid[x + 1][y] == '.':
            x += 1
        else:
            return path
        path.append((x, y))


@timeit
def part_1(paths, infinite_floor=False):
    grid, start_point = build_grid(paths, infinite_floor)

    path = [start_point]
    count = 0

    while path:
        path = get_resting_place(path, grid)
        if not path:
            return count
        x, y = path.pop()
        grid[x][y] = 'o'
        count += 1

    return count


@timeit
def part_2(paths):
    return part_1.func(paths, infinite_floor=True)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
