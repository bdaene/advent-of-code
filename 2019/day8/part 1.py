

from collections import Counter


def solve(input_file, width=25, height=6):
    picture = list(map(int, input_file.readline()[:-1]))

    index, layers = 0, []
    while index < len(picture):
        layer = []
        for _ in range(height):
            row = picture[index:index+width]
            layer.append(row)
            index += width
        layers.append(layer)

    best = None
    for layer in layers:
        count = Counter()
        for row in layer:
            count.update(row)
        if best is None or count[0] < best[0]:
            best = count

    return best[1]*best[2]


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))