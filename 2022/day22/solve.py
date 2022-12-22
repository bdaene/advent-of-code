import numpy
from matplotlib import pyplot
from utils import timeit


@timeit
def get_data():
    board = []
    with open('input.txt') as input_file:
        for line in input_file:
            if line.isspace():
                break
            board.append(' ' + line[:-1] + ' ')
        path = input_file.readline().strip()

    width = max(len(row) for row in board)
    board = tuple(row + ' ' * (width - len(row)) for row in [''] + board + [''])

    path_, digits = [], ""
    for c in path:
        if c == 'L':
            path_.append(int(digits))
            path_.append('L')
            digits = ""
        elif c == 'R':
            path_.append(int(digits))
            path_.append('R')
            digits = ""
        else:
            digits += c
    if digits:
        path_.append(int(digits))

    return board, tuple(path_)


@timeit
def part_1(board, path):
    row, column, direction = 1, board[1].index('.'), 0

    for instruction in path:
        if instruction == 'L':
            direction = (direction - 1) % 4
        elif instruction == 'R':
            direction = (direction + 1) % 4
        else:
            dr, dc = ((0, 1), (1, 0), (0, -1), (-1, 0))[direction]
            for _ in range(instruction):
                row_, column_ = row + dr, column + dc
                if board[row_][column_] == ' ':
                    while True:
                        row_ -= dr
                        column_ -= dc
                        if board[row_][column_] == ' ':
                            row_ += dr
                            column_ += dc
                            break
                if board[row_][column_] != '#':
                    row = row_
                    column = column_

    return row * 1000 + column * 4 + direction


# My input
BOARD = [
    [0, 1, 2],
    [0, 3, 0],
    [4, 5, 0],
    [6, 0, 0]
]
BOARD_SIZE = 50
FACE_POSITIONS = {face: (1 + BOARD_SIZE * row, 1 + BOARD_SIZE * column)
                  for row, line in enumerate(BOARD) for column, face in enumerate(line)
                  if face != 0}

FACES = {
    1: (FACE_POSITIONS[1], ((2, 0), (3, 1), (4, 0), (6, 0))),
    2: (FACE_POSITIONS[2], ((5, 2), (3, 2), (1, 2), (6, 3))),
    3: (FACE_POSITIONS[3], ((2, 3), (5, 1), (4, 1), (1, 3))),
    4: (FACE_POSITIONS[4], ((5, 0), (6, 1), (1, 0), (3, 0))),
    5: (FACE_POSITIONS[5], ((2, 2), (6, 2), (4, 2), (3, 3))),
    6: (FACE_POSITIONS[6], ((5, 3), (2, 1), (1, 1), (4, 3))),
}


# Sample
# BOARD = [
#     [0, 0, 1, 0],
#     [2, 3, 4, 0],
#     [0, 0, 5, 6],
# ]
# BOARD_SIZE = 4
# FACE_POSITIONS = {face: (1 + BOARD_SIZE * row, 1 + BOARD_SIZE * column)
#                   for row, line in enumerate(BOARD) for column, face in enumerate(line)
#                   if face != 0}
#
# FACES = {
#     1: (FACE_POSITIONS[1], ((6, 2), (4, 1), (3, 1), (2, 1))),
#     2: (FACE_POSITIONS[2], ((3, 0), (5, 3), (6, 3), (1, 1))),
#     3: (FACE_POSITIONS[3], ((4, 0), (5, 0), (2, 2), (1, 0))),
#     4: (FACE_POSITIONS[4], ((6, 1), (5, 1), (3, 2), (1, 3))),
#     5: (FACE_POSITIONS[5], ((6, 0), (2, 3), (3, 3), (4, 3))),
#     6: (FACE_POSITIONS[6], ((1, 2), (2, 0), (5, 2), (4, 2))),
# }


def validate_faces():
    for face, (_, neighbors) in FACES.items():
        for direction, (face_, direction_) in enumerate(neighbors):

            if FACES[face_][1][(direction_ + 2) % 4] != (face, (direction + 2) % 4):
                raise ValueError(f"Edge {(face, direction)} does not match edge {(face_, (direction_ + 2) % 4)}.")


validate_faces()


def get_next_state(row, column, direction):
    dr, dc = ((0, 1), (1, 0), (0, -1), (-1, 0))[direction]
    row_ = row + dr
    column_ = column + dc

    face = BOARD[(row - 1) // BOARD_SIZE][(column - 1) // BOARD_SIZE]
    position = FACES[face][0]
    if position[0] <= row_ < position[0] + BOARD_SIZE and position[1] <= column_ < position[1] + BOARD_SIZE:
        return row_, column_, direction

    face = BOARD[(row - 1) // BOARD_SIZE][(column - 1) // BOARD_SIZE]
    face_, direction_ = FACES[face][1][direction]
    position_ = FACES[face_][0]

    face_row, face_col = row_ - position[0] - dr * BOARD_SIZE, column_ - position[1] - dc * BOARD_SIZE

    for _ in range((direction_ - direction) % 4):
        face_row, face_col = face_col, BOARD_SIZE - face_row - 1

    return position_[0] + face_row, position_[1] + face_col, direction_


COLORS = {
    '.': (127, 51, 0),
    ' ': (0, 0, 0),
    '#': (127, 0, 0),
}


def show_board(axes, image, board_path, new_count):
    for row, column, direction in board_path[-new_count - 1:-1]:
        image[row, column] = (63, 63, 63)
    row, column, direction = board_path[-1]
    image[row, column] = (255, 255, 255)

    axes.set_data(image)
    pyplot.draw()
    pyplot.pause(0.01)


@timeit
def part_2(board, path):
    validate_faces()

    row, column, direction = 1, board[1].index('.'), 0
    board_path = [(row, column, direction)]

    image = numpy.asarray([[COLORS[cell] for cell in line] for line in board])
    # axes = pyplot.imshow(image)

    for instruction in path:
        if instruction == 'L':
            direction = (direction - 1) % 4
        elif instruction == 'R':
            direction = (direction + 1) % 4
        else:
            count = 0
            for _ in range(instruction):
                row_, column_, direction_ = get_next_state(row, column, direction)
                if board[row_][column_] == '#':
                    break

                direction = direction_
                row = row_
                column = column_
                board_path.append((row, column, direction))
                count += 1

            # show_board(axes, image, board_path, count)

    return row * 1000 + column * 4 + direction


def main():
    board, path = get_data()
    part_1(board, path)
    part_2(board, path)


if __name__ == "__main__":
    main()
