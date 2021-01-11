import re

from utils import timeit


@timeit
def get_position():
    pattern = re.compile(r'row (\d+), column (\d+).')
    with open('input.txt') as input_file:
        row, column = pattern.search(input_file.readline()).groups()
    return int(row), int(column)


@timeit
def part_1(position, start=20151125, base=252533, mod=33554393):
    row, column = position
    diagonal = row + column - 2
    code_index = diagonal * (diagonal + 1) // 2 + column

    return start * pow(base, code_index - 1, mod) % mod


@timeit
def part_2(position):
    return len(position)


def main():
    position = get_position()
    part_1(position)
    part_2(position)


if __name__ == "__main__":
    main()
