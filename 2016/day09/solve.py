import re
from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return input_file.readline().strip()


pattern = re.compile(r'\((\d+)x(\d+)\)')


@timeit
def part_1(data):

    count = 0
    i = 0
    while i < len(data):
        if data[i] == '(':
            match = pattern.match(data, pos=i)
            a, b = match.groups()
            a, b = int(a), int(b)
            i = match.end() + a
            count += a*b
        else:
            i += 1
            count += 1

    return count


@timeit
def part_2(data):

    def get_len(data_):
        if match := pattern.search(data_):
            a, b = match.groups()
            a, b = int(a), int(b)
            return match.start() + get_len(data_[match.end():match.end() + a]) * b + get_len(data_[match.end() + a:])
        else:
            return len(data_)

    return get_len(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
