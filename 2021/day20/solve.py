import numpy
from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        enhancement = input_file.readline().strip()
        input_file.readline()  # Skip empty line

        picture = []
        for line in input_file:
            picture.append(line.strip())
    return enhancement, tuple(picture)


@timeit
def part_1(data, passes=2):
    enhancement, picture = data

    enhancement = numpy.array([c == '#' for c in enhancement])
    picture = numpy.array([[c == '#' for c in line] for line in picture])
    value_at_infinity = False
    mask = numpy.array([[1 << (8-r * 3 - c) for c in range(3)] for r in range(3)])

    for _ in range(passes):
        new_picture = numpy.full((picture.shape[0] + 4, picture.shape[1] + 4), value_at_infinity)
        new_picture[2:-2, 2:-2] = picture
        pixel_value = numpy.full((picture.shape[0] + 2, picture.shape[1] + 2), 0)
        for (r, c), v in numpy.ndenumerate(mask):
            pixel_value += v * new_picture[r:new_picture.shape[0]-2+r, c:new_picture.shape[0]-2+c]
        picture = enhancement[pixel_value]
        value_at_infinity = enhancement[-1] if value_at_infinity else enhancement[0]

    return picture.sum()


@timeit
def part_2(data):
    return part_1.func(data, 50)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
