

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

    image = layers[0]
    for layer in layers[1:]:
        for row in range(height):
            for col in range(width):
                if image[row][col] == 2:
                    image[row][col] = layer[row][col]

    s = '\n'.join(''.join(' ' if image[row][col] == 0 else '\u2588' for col in range(width)) for row in range(height))
    return s


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))