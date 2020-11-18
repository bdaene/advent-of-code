
from collections import Counter


def solve(input_file):
    coordinates = set()
    for line in input_file:
        x, y = map(int, line.split(','))
        coordinates.add((x, y))
    x_min, x_max = min(coordinates, key=lambda c: c[0])[0], max(coordinates, key=lambda c: c[0])[0]
    y_min, y_max = min(coordinates, key=lambda c: c[1])[1], max(coordinates, key=lambda c: c[1])[1]

    print(x_min, x_max, y_min, y_max)

    count = 0
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            distance = sum(abs(x-c[0]) + abs(y-c[1]) for c in coordinates)
            if distance < 10000:
                count += 1

    return count


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
