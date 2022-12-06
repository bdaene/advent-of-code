from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return input_file.readline()


@timeit
def part_1(data, n=4):
    i = 0
    while len(set(data[i:i + n])) != n:
        i += 1
    return i + n


@timeit
def part_2(data):
    return part_1.func(data, 14)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
