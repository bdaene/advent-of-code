from collections import defaultdict
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            data.append(line.strip())
    return data


@timeit
def part_1(data, nb_burst=10000):
    grid = defaultdict(lambda: '.')

    for r, row in enumerate(data, -(len(data)//2)):
        for c, cell in enumerate(row, -(len(row)//2)):
            grid[(r, c)] = cell

    count = 0
    r, c, dr, dc = 0, 0, -1, 0
    for _ in range(nb_burst):
        if grid[(r, c)] == '#':
            dr, dc = dc, -dr
        else:
            dr, dc = -dc, dr
        if grid[(r, c)] == '#':
            grid[(r, c)] = '.'
        else:
            grid[(r, c)] = '#'
            count += 1
        r += dr
        c += dc

    return count


@timeit
def part_2(data, nb_burst=10000000):
    grid = defaultdict(lambda: '.')

    for r, row in enumerate(data, -(len(data) // 2)):
        for c, cell in enumerate(row, -(len(row) // 2)):
            grid[(r, c)] = cell

    count = 0
    r, c, dr, dc = 0, 0, -1, 0
    for _ in range(nb_burst):
        state = grid[(r, c)]
        if state == '.':
            dr, dc = -dc, dr
            new_state = 'W'
        elif state == 'W':
            count += 1
            new_state = '#'
        elif state == '#':
            dr, dc = dc, -dr
            new_state = 'F'
        elif state == 'F':
            dr, dc = -dr, -dc
            new_state = '.'
        else:
            raise ValueError(f"Unknown state {state}")
        grid[(r, c)] = new_state
        r += dr
        c += dc

    return count


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
