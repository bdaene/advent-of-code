import re
from collections import defaultdict
from utils import timeit


@timeit
def get_data():
    data = []
    pattern = re.compile(r'p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>')
    with open('input.txt') as input_file:
        for line in input_file:
            particle = tuple(map(int, pattern.match(line).groups()))
            data.append((particle[0:3], particle[3:6], particle[6:9]))
    return data


@timeit
def part_1(data):

    def get_size(vector):
        return sum(map(abs, vector))

    particles = sorted(enumerate(data), key=lambda p: (get_size(p[1][2]), get_size(p[1][1]), get_size(p[1][0])))
    return particles[0][0]


@timeit
def part_2(data):

    particles = {i: (x, v, a) for i, (x, v, a) in enumerate(data)}
    while True:
        for i, (x, v, a) in particles.items():
            v = tuple(v_i + a_i for v_i, a_i in zip(v, a))
            x = tuple(x_i + v_i for x_i, v_i in zip(x, v))
            particles[i] = (x, v, a)

        pos = defaultdict(set)
        for i, (x, v, a) in particles.items():
            pos[x].add(i)

        for ps in pos.values():
            if len(ps) > 1:
                for p in ps:
                    del particles[p]

        print(len(particles))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
