from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return input_file.readline().strip().split(',')


@timeit
def part_1(data):

    # u = 'ne', v = 'n', w = 'se' = u-v
    u, v = 0, 0
    for step in data:
        if step == 'n':
            v += 1
        elif step == 'ne':
            u += 1
        elif step == 'se':
            u += 1
            v -= 1
        elif step == 's':
            v -= 1
        elif step == 'sw':
            u -= 1
        elif step == 'nw':
            u -= 1
            v += 1

    w = 0
    if u < 0 < v:
        w = -min(-u, v)
    elif u > 0 > v:
        w = min(u, -v)

    return abs(u-w) + abs(v+w) + abs(w)


@timeit
def part_2(data):

    # u = 'ne', v = 'n', w = 'se' = u-v
    furthest = 0
    u, v = 0, 0
    for i, step in enumerate(data, 1):
        if step == 'n':
            v += 1
        elif step == 'ne':
            u += 1
        elif step == 'se':
            u += 1
            v -= 1
        elif step == 's':
            v -= 1
        elif step == 'sw':
            u -= 1
        elif step == 'nw':
            u -= 1
            v += 1

        w = 0
        if u < 0 < v:
            w = -min(-u, v)
        elif u > 0 > v:
            w = min(u, -v)

        furthest = max(furthest, abs(u-w) + abs(v+w) + abs(w))

    return furthest


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
