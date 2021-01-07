from utils import timeit


@timeit
def get_dimensions():
    dimensions = []
    with open('input.txt') as input_file:
        for line in input_file:
            dimensions.append(tuple(map(int, line.strip().split('x'))))
    return dimensions


@timeit
def part_1(dimensions):
    total = 0
    for l, w, h in dimensions:
        total += 2 * (l * w + h * l + w * h) + min(l * w, h * l, w * h)

    return total


@timeit
def part_2(dimensions):
    total = 0
    for l, w, h in dimensions:
        total += 2 * min(l + w, w + h, h + l) + l * w * h

    return total


def main():
    dimensions = get_dimensions()
    part_1(dimensions)
    part_2(dimensions)


if __name__ == "__main__":
    main()
