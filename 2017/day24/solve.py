from collections import defaultdict
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            x, y = map(int, line.strip().split('/'))
            data.append((x, y))
    return data


@timeit
def part_1(data):

    pins = defaultdict(set)
    for i, (x, y) in enumerate(data):
        pins[x].add(i)
        pins[y].add(i)

    stack = [(0, 0, frozenset(range(len(data))))]
    best = 0
    while stack:
        strength, pin, available_components = stack.pop()
        best = max(best, strength)
        for i in pins[pin] & available_components:
            s = sum(data[i])
            stack.append((strength + s, s - pin, available_components - {i}))

    return best


@timeit
def part_2(data):

    pins = defaultdict(set)
    for i, (x, y) in enumerate(data):
        pins[x].add(i)
        pins[y].add(i)

    stack = [(0, 0, 0, frozenset(range(len(data))))]
    best = (0, 0)
    while stack:
        length, strength, pin, available_components = stack.pop()
        best = max(best, (length, strength))
        for i in pins[pin] & available_components:
            s = sum(data[i])
            stack.append((length + 1, strength + s, s - pin, available_components - {i}))

    return best


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
