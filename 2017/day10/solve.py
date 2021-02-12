from functools import reduce
from operator import xor
from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(map(int, input_file.readline().strip().split(',')))


def apply_round(lengths, current, skip, elements):
    for length in lengths:
        elements = elements[current:] + elements[:current]
        elements = elements[:length][::-1] + elements[length:]
        elements = elements[-current:] + elements[:-current]

        current += length + skip
        current %= len(elements)
        skip += 1
        skip %= len(elements)
    return current, skip, elements


@timeit
def part_1(data, nb_elements=256):

    elements = list(range(nb_elements))
    current, skip, elements = apply_round(data, 0, 0, elements)

    return elements[0]*elements[1]


@timeit
def part_2(data, nb_elements=256, nb_round=64, suffix=(17, 31, 73, 47, 23)):

    current, skip, elements = 0, 0, list(range(nb_elements))
    lengths = tuple(map(ord, ','.join(map(str, data)))) + suffix

    for _ in range(nb_round):
        current, skip, elements = apply_round(lengths, current, skip, elements)

    return ''.join(f"{reduce(xor, elements[i:i+16]):02x}" for i in range(0, nb_elements, 16))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
