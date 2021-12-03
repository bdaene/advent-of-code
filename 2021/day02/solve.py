from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            action, value = line.split()
            data.append((action, int(value)))
    return data


@timeit
def part_1(data):
    horizontal, depth = 0, 0
    for action, value in data:
        if action == 'forward':
            horizontal += value
        elif action == 'down':
            depth += value
        elif action == 'up':
            depth -= value
        else:
            raise ValueError(f'Unknown action: {action}.')

    return horizontal * depth


@timeit
def part_2(data):
    horizontal, depth, aim = 0, 0, 0
    for action, value in data:
        if action == 'forward':
            horizontal += value
            depth += aim * value
        elif action == 'down':
            aim += value
        elif action == 'up':
            aim -= value
        else:
            raise ValueError(f'Unknown action: {action}.')

    return horizontal * depth


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
