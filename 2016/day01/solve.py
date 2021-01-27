from utils import timeit
import turtle


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        return [(token[0], int(token[1:])) for token in input_file.readline().split(', ')]


@timeit
def part_1(data):
    p, d = 0, 1j
    rot = {'R': -1j, 'L': 1j}
    for r, l in data:
        d *= rot[r]
        p += d * l

    return abs(p.real) + abs(p.imag)


@timeit
def part_2(data):
    seen = {0}

    p, d = 0, 1j
    rot = {'R': -1j, 'L': 1j}
    for r, l in data:
        seen.add(p)
        d *= rot[r]

        for _ in range(l):
            p += d
            if p in seen:
                return abs(p.real) + abs(p.imag)
            else:
                seen.add(p)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
