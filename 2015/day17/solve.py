from utils import timeit


@timeit
def get_containers():
    containers = []
    with open('input.txt') as input_file:
        for line in input_file:
            containers.append(int(line))
    return containers


@timeit
def part_1(containers):
    def get_nb_combinations(volume, n):
        if volume < 0:
            return 0
        if volume == 0:
            return 1
        if n == 0:
            return 0

        return get_nb_combinations(volume - containers[n - 1], n - 1) + get_nb_combinations(volume, n - 1)

    return get_nb_combinations(150, len(containers))


@timeit
def part_2(containers):
    def get_nb_combinations(volume, m, n):
        if volume < 0:
            return 0
        if volume == 0:
            return 1
        if n == 0:
            return 0
        if m == 0:
            return 0

        return get_nb_combinations(volume - containers[n - 1], m - 1, n - 1) + get_nb_combinations(volume, m,
                                                                                                   n - 1)

    m = 1
    while get_nb_combinations(150, m, len(containers)) == 0:
        m += 1

    return get_nb_combinations(150, m, len(containers))


def main():
    containers = get_containers()
    part_1(containers)
    part_2(containers)


if __name__ == "__main__":
    main()
