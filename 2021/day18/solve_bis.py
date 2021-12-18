import itertools
import json
from functools import reduce

from utils import timeit


def transform_to_tuple(original_list):
    try:
        return tuple(map(transform_to_tuple, original_list))
    except TypeError:
        return original_list


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(transform_to_tuple(json.loads(line.strip())) for line in input_file)


def add(a, b):
    x = (a, b)
    change = True
    while change:
        _, x, _ = explode(x)
        change, x = split(x)
    return x


def explode(x, depth=4):
    if isinstance(x, int):
        return None, x, None

    a, b = x
    if depth == 0:
        return a, 0, b

    left_part, a, temp_right_part = explode(a, depth - 1)
    b = add_left(b, temp_right_part)
    temp_left_part, b, right_part = explode(b, depth - 1)
    a = add_right(a, temp_left_part)
    return left_part, (a, b), right_part


def add_left(x, value):
    if value is None:
        return x
    if isinstance(x, int):
        return x + value
    a, b = x
    return add_left(a, value), b


def add_right(x, value):
    if value is None:
        return x
    if isinstance(x, int):
        return x + value
    a, b = x
    return a, add_right(b, value)


def split(x):
    if isinstance(x, int):
        if x > 9:
            half = x // 2
            return True, (half, x - half)
        else:
            return False, x
    else:
        change, a = split(x[0])
        if change:
            return change, (a, x[1])
        change, b = split(x[1])
        if change:
            return change, (x[0], b)
        return False, x


def magnitude(x):
    if isinstance(x, int):
        return x
    a, b = x
    return 3 * magnitude(a) + 2 * magnitude(b)


@timeit
def part_1(data):
    total = reduce(add, data)
    return magnitude(total)


@timeit
def part_2(data):
    return max(magnitude(add(a, b)) for a, b in itertools.permutations(data, 2))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
