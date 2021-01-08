import numpy
from utils import timeit


@timeit
def get_grid():
    grid = []
    with open('input.txt') as input_file:
        for line in input_file:
            grid.append(line.strip())
    return grid


@timeit
def part_1(grid, iterations=100, stuck=False):
    grid_ = numpy.full((len(grid), len(grid[0])), False)
    for r, row in enumerate(grid):
        for c, light in enumerate(row):
            grid_[r, c] = light == '#'

    grid = grid_
    for _ in range(iterations):
        count = numpy.full(grid.shape, 0)
        count[:-1, :] += grid[1:, :]
        count[1:, :] += grid[:-1, :]
        count[:, :-1] += grid[:, 1:]
        count[:, 1:] += grid[:, :-1]
        count[:-1, :-1] += grid[1:, 1:]
        count[1:, :-1] += grid[:-1, 1:]
        count[1:, 1:] += grid[:-1, :-1]
        count[:-1, 1:] += grid[1:, :-1]

        grid = (count == 3) | (grid & (count == 2))

        if stuck:
            grid[0, 0] = grid[0, -1] = grid[-1, 0] = grid[-1, -1] = True

    return grid.sum()


@timeit
def part_2(grid):
    return part_1.func(grid, stuck=True)


def main():
    grid = get_grid()
    part_1(grid)
    part_2(grid)


if __name__ == "__main__":
    main()
