import numpy
from utils import timeit


@timeit
def get_grid():
    grid = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            grid.append(value)
    return grid


@timeit
def part_1(grid, cycles=6):
    sky = numpy.zeros((len(grid[0]) + cycles * 2, len(grid) + cycles * 2, 1 + cycles * 2), dtype=bool)
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell == '#':
                sky[cycles + x, cycles + y, cycles] = True

    for _ in range(cycles):
        count = numpy.zeros(sky.shape, dtype=int)

        count[1:, :, :] += sky[:-1, :, :]
        count[:, 1:, :] += sky[:, :-1, :]
        count[:, :, 1:] += sky[:, :, :-1]
        count[:-1, :, :] += sky[1:, :, :]
        count[:, :-1, :] += sky[:, 1:, :]
        count[:, :, :-1] += sky[:, :, 1:]

        count[1:, 1:, :] += sky[:-1, :-1, :]
        count[:, 1:, 1:] += sky[:, :-1, :-1]
        count[1:, :, 1:] += sky[:-1, :, :-1]
        count[1:, :-1, :] += sky[:-1, 1:, :]
        count[:, 1:, :-1] += sky[:, :-1, 1:]
        count[:-1, :, 1:] += sky[1:, :, :-1]
        count[:-1, :-1, :] += sky[1:, 1:, :]
        count[:, :-1, :-1] += sky[:, 1:, 1:]
        count[:-1, :, :-1] += sky[1:, :, 1:]
        count[:-1, 1:, :] += sky[1:, :-1, :]
        count[:, :-1, 1:] += sky[:, 1:, :-1]
        count[1:, :, :-1] += sky[:-1, :, 1:]

        count[1:, 1:, 1:] += sky[:-1, :-1, :-1]
        count[1:, 1:, :-1] += sky[:-1, :-1, 1:]
        count[1:, :-1, 1:] += sky[:-1, 1:, :-1]
        count[1:, :-1, :-1] += sky[:-1, 1:, 1:]
        count[:-1, 1:, 1:] += sky[1:, :-1, :-1]
        count[:-1, 1:, :-1] += sky[1:, :-1, 1:]
        count[:-1, :-1, 1:] += sky[1:, 1:, :-1]
        count[:-1, :-1, :-1] += sky[1:, 1:, 1:]

        # print(count)

        sky = (count == 3) | (sky & (count == 2))

        for z in range(sky.shape[2]):
            print('\n'.join(''.join('#' if sky[x, y, z] else '.' for x in range(sky.shape[0])) for y in
                            range(sky.shape[1])))
            print()

    return sky.sum()


@timeit
def part_2(grid, cycles=6):
    sky = numpy.zeros((len(grid[0]) + cycles * 2, len(grid) + cycles * 2, 1 + cycles * 2, 1 + cycles * 2),
                      dtype=bool)
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell == '#':
                sky[cycles + x, cycles + y, cycles, cycles] = True

    for _ in range(cycles):
        count = numpy.zeros(sky.shape, dtype=int)

        for xl, xr in ((slice(0, sky.shape[0] - 1), slice(1, sky.shape[0])),
                       (slice(0, sky.shape[0]), slice(0, sky.shape[0])),
                       (slice(1, sky.shape[0]), slice(0, sky.shape[0] - 1))):
            for yl, yr in ((slice(0, sky.shape[1] - 1), slice(1, sky.shape[1])),
                           (slice(0, sky.shape[1]), slice(0, sky.shape[1])),
                           (slice(1, sky.shape[1]), slice(0, sky.shape[1] - 1))):
                for zl, zr in ((slice(0, sky.shape[2] - 1), slice(1, sky.shape[2])),
                               (slice(0, sky.shape[2]), slice(0, sky.shape[2])),
                               (slice(1, sky.shape[2]), slice(0, sky.shape[2] - 1))):
                    for wl, wr in ((slice(0, sky.shape[3] - 1), slice(1, sky.shape[3])),
                                   (slice(0, sky.shape[3]), slice(0, sky.shape[3])),
                                   (slice(1, sky.shape[3]), slice(0, sky.shape[3] - 1))):
                        count[xl, yl, zl, wl] += sky[xr, yr, zr, wr]

        count -= sky
        sky = (count == 3) | (sky & (count == 2))

    return sky.sum()


def main():
    grid = get_grid()
    part_1(grid)
    part_2(grid)


if __name__ == "__main__":
    main()
