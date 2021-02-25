from utils import timeit, DisjointSets


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(tuple(map(int, line.split(','))) for line in input_file.readlines())


@timeit
def part_1(data):

    constellations = DisjointSets()

    for i, point_a in enumerate(data):
        constellations.make_set(point_a)
        for point_b in data[:i]:
            if sum(abs(a-b) for a, b in zip(point_a, point_b)) <= 3:
                constellations.merge(point_a, point_b)

    for point in data:
        constellations.find(point)

    return len(set(constellations.node_parents.values()))


def main():
    data = get_data()
    part_1(data)


if __name__ == "__main__":
    main()
