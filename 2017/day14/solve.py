from functools import reduce
from operator import xor
from utils import timeit, DisjointSets


def get_knot_hash(data):

    lengths = tuple(map(ord, data)) + (17, 31, 73, 47, 23)
    current, skip, elements = 0, 0, list(range(256))

    for _ in range(64):
        for length in lengths:
            elements = elements[current:] + elements[:current]
            elements = elements[:length][::-1] + elements[length:]
            elements = elements[-current:] + elements[:-current]

            current += length + skip
            current %= len(elements)
            skip += 1
            skip %= len(elements)

    return ''.join(f"{reduce(xor, elements[i:i+16]):02x}" for i in range(0, 256, 16))


@timeit
def part_1(data):
    count = 0
    for row in range(128):
        hashed_row = get_knot_hash(f"{data}-{row}")
        value = int(hashed_row, 16)
        while value > 0:
            if value & 1:
                count += 1
            value >>= 1
    return count


def get_grid(seed):
    grid = []
    for row in range(128):
        hashed_row = int(get_knot_hash(f"{seed}-{row}"), 16)
        grid_row = []
        for col in range(128):
            hashed_row, value = divmod(hashed_row, 2)
            grid_row.append('#' if value == 1 else '.')
        grid.append(grid_row[::-1])
    return grid


def show_regions(grid, regions):
    regions_name = {}
    named_grid = []
    for row in range(128):
        named_row = []
        for col in range(128):
            if grid[row][col] == '.':
                named_row.append('.')
            else:
                region = regions.find((row, col))
                if region not in regions_name:
                    regions_name[region] = chr(48 + len(regions_name) % (122-48))
                named_row.append(regions_name[region])
        named_grid.append(named_row)

    print('\n'.join(''.join(named_row) for named_row in named_grid))


@timeit
def part_2(data):

    grid = get_grid(data)
    regions = DisjointSets()

    for row in range(128):
        for col in range(128):
            if grid[row][col] == '#':
                regions.make_set((row, col))
                if row > 0 and grid[row-1][col] == '#':
                    regions.merge((row, col), (row-1, col))
                if col > 0 and grid[row][col-1] == '#':
                    regions.merge((row, col), (row, col-1))

    # show_regions(grid, regions)

    return len(regions)


def main():
    data = 'vbqugkhl'
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
