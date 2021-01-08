import numpy
from utils import timeit


@timeit
def part_1(target=29000000, nb_house=10 ** 6):
    houses = numpy.full(nb_house, 0)
    e = 0
    while houses[e] < target:
        e += 1
        houses[e::e] += e * 10

    return e


@timeit
def part_2(target=29000000, nb_house=10 ** 6):
    houses = numpy.full(nb_house, 0)
    e = 0
    while houses[e] < target:
        e += 1
        houses[e:e * 51:e] += e * 11

    return e


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
