
from collections import Counter


def solve(input_file):
    coordinates = set()
    for line in input_file:
        x, y = map(int, line.split(','))
        coordinates.add((x, y))
    x_min, x_max = min(coordinates, key=lambda c: c[0])[0], max(coordinates, key=lambda c: c[0])[0]
    y_min, y_max = min(coordinates, key=lambda c: c[1])[1], max(coordinates, key=lambda c: c[1])[1]

    print(x_min, x_max, y_min, y_max)

    count = Counter()
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            closest_distance = abs(x_min) + abs(x_max) + abs(y_max) + abs(y_min)
            closest_coordinates = []
            for coordinate in coordinates:
                distance = abs(x-coordinate[0]) + abs(y-coordinate[1])
                if distance < closest_distance:
                    closest_distance = distance
                    closest_coordinates = [coordinate]
                elif distance == closest_distance:
                    closest_coordinates.append(coordinate)
            if len(closest_coordinates) > 1:
                continue
            closest_coordinate = closest_coordinates[0]
            if count[closest_coordinate] < 0:
                continue
            if x == x_min or x == x_max or y == y_min or y == y_max:
                count[closest_coordinate] = -1
            else:
                count[closest_coordinate] += 1

    print(count)
    return max(count.values())


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
