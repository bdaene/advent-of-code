from utils import timeit


@timeit
def part_1(trees):
    position = 0
    count = 0
    for line in trees[1:]:
        position += 3
        if line[position % len(line)] == '#':
            count += 1
    return count


@timeit
def part_2(trees):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = []
    total = 1

    for r, d in slopes:
        position = 0
        count = 0
        for line in trees[d::d]:
            position += r
            if line[position % len(line)] == '#':
                count += 1
        counts.append(count)
        total *= count

    print(counts)
    return total


def main():
    with open('input.txt') as input_file:
        trees = [line.strip() for line in input_file]

    part_1(trees)
    part_2(trees)


if __name__ == "__main__":
    main()
