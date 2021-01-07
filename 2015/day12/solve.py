from json import load

from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return load(input_file)


@timeit
def part_1(data):
    def get_sum(o):
        if isinstance(o, list):
            return sum(map(get_sum, o))
        elif isinstance(o, dict):
            return sum(map(get_sum, o.keys())) + sum(map(get_sum, o.values()))
        elif isinstance(o, str):
            return 0
        else:
            return o

    return get_sum(data)


@timeit
def part_2(data):
    def get_sum(o):
        if isinstance(o, list):
            return sum(map(get_sum, o))
        elif isinstance(o, dict):
            if 'red' in o.values():
                return 0
            else:
                return sum(map(get_sum, o.keys())) + sum(map(get_sum, o.values()))
        elif isinstance(o, str):
            return 0
        else:
            return o

    return get_sum(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
