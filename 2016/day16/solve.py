from itertools import chain
from utils import timeit


@timeit
def part_1(data, disc_length=272):

    while len(data) < disc_length:
        data = ''.join(chain(data, '0', ('0' if c == '1' else '1' for c in reversed(data))))

    data = data[:disc_length]
    while len(data) % 2 == 0:
        data = ''.join('1' if data[i] == data[i+1] else '0' for i in range(0, len(data), 2))

    return data


@timeit
def part_2(data):
    return part_1.func(data, disc_length=35651584)


def main():
    data = '10010000000110000'
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
