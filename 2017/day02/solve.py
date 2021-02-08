from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            data.append(tuple(map(int, line.split())))
    return data


@timeit
def part_1(data):
    return sum(max(line)-min(line) for line in data)


@timeit
def part_2(data):

    def get_value(line):
        for i, a in enumerate(line):
            for b in line[i+1:]:
                if a > b:
                    d, r = divmod(a, b)
                else:
                    d, r = divmod(b, a)
                if r == 0:
                    return d

    return sum(map(get_value, data))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
