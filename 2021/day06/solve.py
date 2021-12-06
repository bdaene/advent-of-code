from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(map(int, input_file.readline().split(',')))


@timeit
def part_1(data, days=80):
    count = [0]*(days+9)
    for counter in data:
        count[counter] += 1

    for day in range(days):
        count[day+9] = count[day]
        count[day+7] += count[day]

    return sum(count[days:])


@timeit
def part_2(data):
    return part_1.func(data, days=256)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
