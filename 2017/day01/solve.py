from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return input_file.readline().strip()


@timeit
def part_1(data):
    return sum(int(a) for a, b in zip(data, data[1:] + data[0]) if a == b)


@timeit
def part_2(data):
    m = len(data)//2
    return sum(int(a) for a, b in zip(data, data[m:] + data[:m]) if a == b)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
