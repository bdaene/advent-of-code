from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            data.append(line[:-1])
    return tuple(data)


@timeit
def part_1(data):
    x, y = data[0].index('|'), 0
    dx, dy = 0, 1

    path = []
    while True:
        if 'A' <= data[y][x] <= 'Z':
            path.append(data[y][x])

        if data[y+dy][x+dx] != ' ':
            pass
        elif data[y+dx][x-dy] != ' ':
            # Turn left
            dx, dy = -dy, dx
        elif data[y-dx][x+dy] != ' ':
            # Turn right
            dx, dy = dy, -dx
        else:
            # No path
            return ''.join(path)
        x += dx
        y += dy


@timeit
def part_2(data):
    x, y = data[0].index('|'), 0
    dx, dy = 0, 1

    steps = 1
    while True:
        if data[y+dy][x+dx] != ' ':
            pass
        elif data[y+dx][x-dy] != ' ':
            # Turn left
            dx, dy = -dy, dx
        elif data[y-dx][x+dy] != ' ':
            # Turn right
            dx, dy = dy, -dx
        else:
            # No path
            return steps
        x += dx
        y += dy
        steps += 1


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
