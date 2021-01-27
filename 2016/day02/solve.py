from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


@timeit
def part_1(data):
    key_pad = [[i*3+j+1 for j in range(3)] for i in range(3)]
    x, y = 1, 1
    code = 0
    for line in data:
        for move in line:
            if move == 'U':
                if y > 0:
                    y -= 1
            elif move == 'D':
                if y < 2:
                    y += 1
            elif move == 'L':
                if x > 0:
                    x -= 1
            elif move == 'R':
                if x < 2:
                    x += 1
            else:
                raise ValueError('Unknown direction.')

        code *= 10
        code += key_pad[y][x]

    return code


@timeit
def part_2(data):

    key_pad = ( "#######",
                "###1###",
                "##234##",
                "#56789#",
                "##ABC##",
                "###D###",
                "#######")

    row, col = 3, 1
    code = []
    for line in data:
        for move in line:
            if move == 'U':
                if key_pad[row-1][col] != '#':
                    row -= 1
            elif move == 'D':
                if key_pad[row+1][col] != '#':
                    row += 1
            elif move == 'L':
                if key_pad[row][col-1] != '#':
                    col -= 1
            elif move == 'R':
                if key_pad[row][col+1] != '#':
                    col += 1

        code.append(key_pad[row][col])

    return ''.join(code)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
