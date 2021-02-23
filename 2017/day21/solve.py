import numpy
import re
from utils import timeit


@timeit
def get_data():
    data = {}
    pattern = re.compile(r'(.*) => (.*)')
    with open('input.txt') as input_file:
        for line in input_file:
            rule, result = pattern.match(line).groups()
            data[rule] = result
    return data


@timeit
def part_1(data, nb_iterations=5):

    def get_key(array):
        return tuple(map(tuple, array))

    rules = {}
    for rule, result in data.items():
        rules[get_key(rule.split('/'))] = numpy.array(get_key(result.split('/')))

    def get_result(array):
        for _ in range(4):
            for _ in range(2):
                if get_key(array) in rules:
                    return rules[get_key(array)]
                array = numpy.flipud(array)
            array = numpy.rot90(array)
        raise ValueError(f"{array} does not match nay rule.")

    start = '.#./..#/###'
    grid = numpy.array(get_key(start.split('/')))

    for _ in range(nb_iterations):
        if grid.shape[0] % 2 == 0:
            chunk_size = 2
        elif grid.shape[0] % 3 == 0:
            chunk_size = 3
        else:
            raise ValueError(f"No rule for {grid.shape} grids.")

        new_size = grid.shape[0]//chunk_size*(chunk_size+1)
        grid_ = numpy.full((new_size, new_size), '.')

        for r in range(grid.shape[0] // chunk_size):
            for c in range(grid.shape[1] // chunk_size):
                grid_[r*(chunk_size+1):(r+1)*(chunk_size+1), c*(chunk_size+1):(c+1)*(chunk_size+1)] = get_result(
                    grid[r*chunk_size:(r+1)*chunk_size, c*chunk_size:(c+1)*chunk_size])

        grid = grid_

    return (grid == '#').sum()


@timeit
def part_2(data):
    return part_1.func(data, nb_iterations=18)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
