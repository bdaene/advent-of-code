import re
from euclide import solve_chinese_remainders
from utils import timeit


@timeit
def get_data():
    data = []
    pattern = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).')
    with open('input.txt') as input_file:
        for line in input_file:
            disc, nb_positions, offset = pattern.match(line).groups()
            data.append((int(disc), int(nb_positions), int(offset)))
    return data


@timeit
def part_1(data):
    # For each disc t+disc+offset = 0 (mod nb_positions)

    remainders = [(-disc-offset, nb_positions) for disc, nb_positions, offset in data]
    t = solve_chinese_remainders(remainders)

    return t


@timeit
def part_2(data):
    return part_1.func(data + [(data[-1][0]+1, 11, 0)])


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
