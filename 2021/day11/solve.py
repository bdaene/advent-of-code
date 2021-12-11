import numpy
from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return numpy.array(tuple(tuple(map(int, line.strip())) for line in input_file))


@timeit
def part_1(data, steps=100):
    grid = data.copy()

    total = 0
    for _ in range(steps):
        grid += 1
        flashes = numpy.full(grid.shape, False)

        while True:
            new_flashes = (grid > 9) & ~flashes
            if not new_flashes.any():
                break
            flashes |= new_flashes

            grid[1:, :] += new_flashes[:-1, :]
            grid[:-1, :] += new_flashes[1:, :]
            grid[:, 1:] += new_flashes[:, :-1]
            grid[:, :-1] += new_flashes[:, 1:]
            grid[1:, 1:] += new_flashes[:-1, :-1]
            grid[1:, :-1] += new_flashes[:-1, 1:]
            grid[:-1, 1:] += new_flashes[1:, :-1]
            grid[:-1, :-1] += new_flashes[1:, 1:]

        grid[flashes] = 0

        total += flashes.sum()

    return total


@timeit
def part_2(data):
    grid = data.copy()

    step = 0
    while not (grid == 0).all():
        grid += 1
        flashes = numpy.full(grid.shape, False)

        while True:
            new_flashes = (grid > 9) & ~flashes
            if not new_flashes.any():
                break
            flashes |= new_flashes

            grid[1:, :] += new_flashes[:-1, :]
            grid[:-1, :] += new_flashes[1:, :]
            grid[:, 1:] += new_flashes[:, :-1]
            grid[:, :-1] += new_flashes[:, 1:]
            grid[1:, 1:] += new_flashes[:-1, :-1]
            grid[1:, :-1] += new_flashes[:-1, 1:]
            grid[:-1, 1:] += new_flashes[1:, :-1]
            grid[:-1, :-1] += new_flashes[1:, 1:]

        grid[flashes] = 0

        step += 1

    return step


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
