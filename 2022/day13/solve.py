from utils import timeit


@timeit
def get_data():
    data, lines = [], []
    with open('input.txt') as input_file:
        for line in input_file:
            if line.isspace():
                data.append(tuple(lines))
                lines = []
            else:
                lines.append(eval(line.strip()))
        data.append(tuple(lines))
    return tuple(data)


def is_in_order(left, right):
    stack = [(left, right)]
    while stack:
        left, right = stack.pop()

        if left == right:
            continue

        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return True
            if left > right:
                return False

        if not isinstance(left, list):
            left = [left]
        if not isinstance(right, list):
            right = [right]

        if left == right:
            continue

        if len(left) == 0:
            return True
        if len(right) == 0:
            return False

        stack.append((left[1:], right[1:]))
        stack.append((left[0], right[0]))


@timeit
def part_1(data):
    total = 0
    for i, (left, right) in enumerate(data, 1):
        if is_in_order(left, right):
            total += i

    return total


@timeit
def part_2(data, dividers=([[2]], [[6]])):
    packets = list(dividers)
    for left, right in data:
        packets.append(left)
        packets.append(right)

    total = 1
    for right in dividers:
        total *= 1 + sum(is_in_order(left, right) for left in packets if left != right)

    return total


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
