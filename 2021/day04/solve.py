from utils import timeit
import numpy


# @timeit
def get_data():
    with open('input.txt') as input_file:
        numbers = tuple(map(int, input_file.readline().strip().split(',')))
        input_file.readline()   # Skip empty line

        grids = []
        while True:
            grid = tuple(tuple(map(int, input_file.readline().split())) for _ in range(5))
            input_file.readline()

            if not grid[0]:
                break
            grids.append(numpy.array(grid))

    return numbers, tuple(grids)


def get_number_to_grid(grids):
    number_to_grid = {}
    for grid_index, grid in enumerate(grids):
        for row, line in enumerate(grid):
            for col, number in enumerate(line):
                number_to_grid.setdefault(number, set()).add((grid_index, row, col))
    return number_to_grid


def add_number(number, grids, number_to_grid, grid_to_checked_numbers):
    won_grids = set()
    for grid_index, row, col in number_to_grid[number]:
        checked_numbers = grid_to_checked_numbers[grid_index]
        checked_numbers.add(number)
        if set(grids[grid_index][row, :]) <= checked_numbers or set(grids[grid_index][:, col]) <= checked_numbers:
            won_grids.add(grid_index)
    return won_grids


@timeit
def part_1(data):
    numbers, grids = data

    number_to_grid = get_number_to_grid(grids)
    grid_to_checked_numbers = [set() for _ in grids]

    for number in numbers:
        won_grids = add_number(number, grids, number_to_grid, grid_to_checked_numbers)
        if won_grids:
            grid_index = won_grids.pop()
            return (grids[grid_index].sum() - sum(grid_to_checked_numbers[grid_index])) * number


@timeit
def part_2(data):
    numbers, grids = data

    number_to_grid = get_number_to_grid(grids)
    grid_to_checked_numbers = [set() for _ in grids]
    all_won_grids = set()

    for number in numbers:
        won_grids = add_number(number, grids, number_to_grid, grid_to_checked_numbers)
        new_won_grids = won_grids - all_won_grids
        all_won_grids |= won_grids
        if len(all_won_grids) == len(grids):
            grid_index = new_won_grids.pop()
            return (grids[grid_index].sum() - sum(grid_to_checked_numbers[grid_index])) * number


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
