from collections import Counter

from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return input_file.readline()


@timeit
def part_1(data, n=4):
    letters = Counter(data[:n])
    count = len(letters)
    if count == n:
        return n

    for i, (a, b) in enumerate(zip(data, data[n:]), n + 1):
        if letters[b] == 0:
            count += 1
        letters[b] += 1
        letters[a] -= 1
        if letters[a] == 0:
            count -= 1
        if count == n:
            return i


@timeit
def part_2(data):
    return part_1.func(data, 14)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
