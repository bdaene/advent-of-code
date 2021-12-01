from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = int(line.strip())
            data.append(value)
    return data


@timeit
def part_1(data):
    return sum(a < b for a, b in zip(data, data[1:]))


@timeit
def part_2(data):
    return sum(a < b for a, b in zip(data, data[3:]))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
