from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return input_file.readline().strip()


@timeit
def part_1(data, nb_rows=40):

    count = 0
    for _ in range(nb_rows):
        count += sum(1 for c in data if c == '.')
        data = ''.join('^' if left != right else '.' for left, right in zip('.' + data[:-1], data[1:] + '.'))

    return count


@timeit
def part_2(data):
    return part_1.func(data, nb_rows=400000)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
