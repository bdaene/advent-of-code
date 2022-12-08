import numpy
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            data.append(tuple(map(int, line.strip())))
    return numpy.array(data)


def compute_visibility(trees):
    visible = numpy.full(trees.shape, False)
    visible[0, :] = True
    height = trees[0, :]
    for i in range(1, trees.shape[0]):
        visible[i, :] |= trees[i, :] > height
        height = numpy.maximum(height, trees[i, :])
    return visible


@timeit
def part_1(data):
    visible = numpy.full(data.shape, False)
    for k in range(4):
        visible |= numpy.rot90(compute_visibility(numpy.rot90(data, k)), -k)
    return visible.sum()


def compute_viewing_distance(trees):
    viewing_distance = numpy.full(trees.shape, 0)
    for tree_row, view_row in zip(trees, viewing_distance):
        tree_heights = [(max(tree_row), 0)]
        for tree_index, tree in enumerate(tree_row):
            while tree_heights[-1][0] < tree:
                tree_heights.pop()
            view_row[tree_index] = tree_index - tree_heights[-1][1]
            tree_heights.append((tree, tree_index))
    return viewing_distance


@timeit
def part_2(data):
    viewing_distance = numpy.full(data.shape, 1)
    for k in range(4):
        viewing_distance *= numpy.rot90(compute_viewing_distance(numpy.rot90(data, k)), -k)
    return viewing_distance.max()


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
