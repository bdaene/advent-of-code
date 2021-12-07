from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(map(int, input_file.readline().split(',')))


@timeit
def part_1(data):
    horizontal = sorted(data)[len(data)//2]
    return sum(abs(x-horizontal) for x in data)


@timeit
def part_2(data):
    horizontal = sum(data)//len(data)
    return min(sum(d*(d+1)//2 for d in (abs(x-h) for x in data)) for h in (horizontal, horizontal+1))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
