from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


def from_snafu(snafu):
    n = 0
    for c in snafu:
        n *= 5
        n += '=-012'.index(c) - 2
    return n


def to_snafu(n):
    snafu = ''
    while n > 0:
        n, r = divmod(n, 5)
        snafu += '012=-'[r]
        if r > 2:
            n += 1
    return snafu[::-1]


@timeit
def part_1(data):
    return to_snafu(sum(map(from_snafu, data)))


@timeit
def part_2(data):
    return len(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
