from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(line.strip() for line in input_file)


@timeit
def analyze(data):
    instructions = []
    for instruction in data:
        if instruction.startswith('inp'):
            instructions.append([])
        instructions[-1].append(instruction)

    with open('input_analysis.txt', 'w') as output_file:
        print('\n'.join(''.join(f'{instruction:<10}' for instruction in part) for part in instructions),
              file=output_file)

    # Each part can be summarized as
    # w = a
    # x = (z%26+c) != a
    # z //= b
    # if x:
    #   y = a + d
    #   z *= 26
    #   z += a + d
    # else:
    #   y = 0

    b_values = tuple(int(part[4].split()[2]) for part in instructions)
    c_values = tuple(int(part[5].split()[2]) for part in instructions)
    d_values = tuple(int(part[15].split()[2]) for part in instructions)

    return b_values, c_values, d_values


def execute_part(a, b, c, d, z):
    x = z % 26 + c
    z //= b
    if x != a:
        z *= 26
        z += a + d
    print(''.join(f'{v:10d}' for v in (b, a - (x + c), a, z)))
    return z


def validate(a_values, b_values, c_values, d_values):
    z = 0
    for a, b, c, d in zip(a_values, b_values, c_values, d_values):
        z = execute_part(a, b, c, d, z)
    return z == 0


@timeit
def part_1(b_values, c_values, d_values, reverse=True):
    def solve(i=0, z=0):
        if i >= 14:
            if z == 0:
                yield ()
                return
        b, c, d = b_values[i], c_values[i], d_values[i]
        x = z % 26 + c
        z //= b
        if 1 <= x <= 9:
            for s in solve(i + 1, z):
                yield (x,) + s
        else:
            if b == 26:
                return
            z *= 26
            z += d
            for a in (range(9, 0, -1) if reverse else range(1, 10)):
                for s in solve(i + 1, z + a):
                    yield (a,) + s

    for a_values in solve():
        if validate(a_values, b_values, c_values, d_values):
            return ''.join(f'{v}' for v in a_values)


@timeit
def part_2(*values):
    return part_1.func(*values, reverse=False)


def main():
    data = get_data()
    values = analyze(data)
    part_1(*values)
    part_2(*values)


if __name__ == "__main__":
    main()
