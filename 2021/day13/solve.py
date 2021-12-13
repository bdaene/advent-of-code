import numpy
import re
from utils import timeit


@timeit
def get_data():
    pattern = re.compile(r'fold along (\w)=(\d+)')
    with open('input.txt') as input_file:
        dots = []
        line = input_file.readline().strip()
        while not line.isspace():
            dots.append(tuple(map(int, line.split(','))))
            line = input_file.readline()

        instructions = []
        for line in input_file:
            axis, pos = pattern.match(line).groups()
            instructions.append((axis, int(pos)))

        return dots, instructions


def create_paper(dots, instructions):
    size_x = max(instruction[1] for instruction in instructions if instruction[0] == 'x') * 2 + 1
    size_y = max(instruction[1] for instruction in instructions if instruction[0] == 'y') * 2 + 1

    paper = numpy.full((size_y, size_x), False)
    paper[tuple(zip(*dots))[::-1]] = True

    return paper


def fold(paper, instructions):
    for axis, pos in instructions:
        if axis == 'y':
            paper = paper[:pos, :] | paper[pos+1:, :][::-1, :]
        elif axis == 'x':
            paper = paper[:, :pos] | paper[:, pos+1:][:, ::-1]
        else:
            raise ValueError(f"Unknown axis {axis}")

    return paper


@timeit
def part_1(data):
    dots, instructions = data
    paper = create_paper(dots, instructions)
    paper = fold(paper, instructions[:1])
    return paper.sum()


@timeit
def part_2(data):
    dots, instructions = data
    paper = create_paper(dots, instructions)
    paper = fold(paper, instructions)
    print('\n'.join(''.join('#' if dot else ' ' for dot in line) for line in paper))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
