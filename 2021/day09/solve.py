import numpy
from utils import timeit, DisjointSets


@timeit
def get_data():
    with open('input.txt') as input_file:
        data = [list(map(int, line.strip())) for line in input_file]
        return numpy.array(data)


@timeit
def part_1(data):
    lowest = numpy.full(data.shape, True)
    lowest[1:, :] &= data[1:, :] < data[:-1, :]
    lowest[:-1, :] &= data[:-1, :] < data[1:, :]
    lowest[:, 1:] &= data[:, 1:] < data[:, :-1]
    lowest[:, :-1] &= data[:, :-1] < data[:, 1:]
    return (lowest * (data + 1)).sum()


@timeit
def part_2(data):
    basins = DisjointSets()
    for row, line in enumerate(data[:-1]):
        for col, cell in enumerate(line[:-1]):
            if cell < 9:
                basins.make_set((row, col))
                if data[row + 1, col] < 9:
                    basins.make_set((row + 1, col))
                    basins.merge((row, col), (row + 1, col))
                if data[row, col + 1] < 9:
                    basins.make_set((row, col + 1))
                    basins.merge((row, col), (row, col + 1))

    basins_size = sorted(basins.node_sizes[node] for node, parent in basins.node_parents.items() if node == parent)
    return basins_size[-1] * basins_size[-2] * basins_size[-3]


@timeit
def part_2_bis(data):
    def find_basin_size(start):
        seen = {start}
        to_explore = [start]
        while to_explore:
            row, col = to_explore.pop()
            for r, c in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
                if 0 <= r < data.shape[0] and 0 <= c < data.shape[1] and data[r, c] < 9 and (r, c) not in seen:
                    seen.add((r, c))
                    to_explore.append((r, c))
        return len(seen)

    lowest = numpy.full(data.shape, True)
    lowest[1:, :] &= data[1:, :] < data[:-1, :]
    lowest[:-1, :] &= data[:-1, :] < data[1:, :]
    lowest[:, 1:] &= data[:, 1:] < data[:, :-1]
    lowest[:, :-1] &= data[:, :-1] < data[:, 1:]

    basins_size = sorted(find_basin_size((row, col)) for row, col in zip(*numpy.where(lowest)))
    return basins_size[-1] * basins_size[-2] * basins_size[-3]


def main():
    data = get_data()
    part_1(data)
    part_2(data)
    part_2_bis(data)


if __name__ == "__main__":
    main()
