import re
from math import gcd
from utils import timeit


@timeit
def get_data():
    data = {}
    pattern = re.compile(r'(\d+): (\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            layer_depth, layer_range = pattern.match(line).groups()
            data[int(layer_depth)] = int(layer_range)
    return data


@timeit
def part_1(data):
    total = 0
    for time in data:
        if time % (2*data[time]-2) == 0:
            total += time * data[time]

    return total


@timeit
def part_2(data):

    delay = 0
    while any((time + delay) % (2*data[time]-2) == 0 for time in data):
        delay += 1

    return delay


@timeit
def part_2_bis(data):

    delays = {0}
    mod = 1
    for layer_depth, layer_range in data.items():
        # caught if delay + layer_depth % (2* layer_range - 2) == 0
        m = layer_range * 2 - 2
        d = gcd(mod, m)
        delays_ = set()
        for i in range(m//d):
            for delay in delays:
                delays_.add(delay + i*mod)
        delays = set(delay for delay in delays_ if delay % m != -layer_depth % m)
        mod *= m//d

    return min(delays)


def main():
    data = get_data()
    part_1(data)
    # part_2(data)
    part_2_bis(data)


if __name__ == "__main__":
    main()
