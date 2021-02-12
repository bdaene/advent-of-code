from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(map(int, input_file.readline().split()))


@timeit
def part_1(data):
    seen = set()
    count = 0
    while data not in seen:
        seen.add(data)
        count += 1
        data = list(data)
        index = 0
        for i, v in enumerate(data[1:], 1):
            if v > data[index]:
                index = i
        nb_blocks = data[index]
        data[index] = 0
        while nb_blocks > 0:
            index += 1
            index %= len(data)
            data[index] += 1
            nb_blocks -= 1

        data = tuple(data)

    return count, data


@timeit
def part_2(data):
    count, data = part_1.func(data)
    return part_1.func(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
