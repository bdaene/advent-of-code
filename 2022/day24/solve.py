from collections import defaultdict
from heapq import heappop, heappush

from utils import timeit


@timeit
def get_data():
    # >v<^
    blizzards = (defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set))
    with open('input.txt') as input_file:
        start = input_file.readline()[1:-1].index('.')

        for row, line in enumerate(input_file):
            for column, cell in enumerate(line[1:-1]):
                if cell in '><':
                    blizzards['>v<^'.index(cell)][row].add(column)
                if cell in 'v^':
                    blizzards['>v<^'.index(cell)][column].add(row)

        end = line[1:-1].index('.')
    return blizzards, start, end, row, column


def show(blizzards, moves, position, height, width):
    print(f"Minute {moves}:")
    board = ["#" * (width + 2)]
    for row in range(height):
        line = '#'
        for column in range(width):
            blizzard = ''
            if (column - moves) % width in blizzards[0][row]:
                blizzard += '>'
            if (row - moves) % height in blizzards[1][column]:
                blizzard += 'v'
            if (column + moves) % width in blizzards[2][row]:
                blizzard += '<'
            if (row + moves) % height in blizzards[3][column]:
                blizzard += '^'

            cell = 'E' if (row, column) == position else '.'
            if blizzard:
                if len(blizzard) > 1:
                    blizzard = str(len(blizzard))
                cell = blizzard
            line += cell
        board.append(line + '#')
    board.append('#' * (width + 2))
    print('\n'.join(board))


def find_best_path(blizzards, height, width, start, end, moves=0):
    start_row, start_column = start
    end_row, end_column = end

    heap: list[tuple[int, int, int, int]]
    heap = [(moves + abs(end_row - start_row) + abs(end_column - start_column), moves, start_row, start_column)]
    seen = set()
    while heap:
        _, moves, row, column = heappop(heap)
        # show(blizzards, moves, (row, column), height, width)

        moves += 1
        for row_, column_ in (
                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1),
                (row, column),
        ):
            if row_ == end_row and column_ == end_column:
                return moves

            if row_ == start_row and column_ == start_column:
                heappush(heap, (moves + abs(end_row - row_) + abs(end_column - column_), moves, row_, column_))

            if not (0 <= row_ < height and 0 <= column_ < width):
                continue

            if (moves, row_, column_) in seen:
                continue

            if (column_ - moves) % width in blizzards[0][row_]:
                continue
            if (row_ - moves) % height in blizzards[1][column_]:
                continue
            if (column_ + moves) % width in blizzards[2][row_]:
                continue
            if (row_ + moves) % height in blizzards[3][column_]:
                continue

            heappush(heap, (moves + abs(end_row - row_) + abs(end_column - column_), moves, row_, column_))
            seen.add((moves, row_, column_))


@timeit
def part_1(blizzards, start_column, end_column, height, width):
    start = (-1, start_column)
    end = (height, end_column)

    return find_best_path(blizzards, height, width, start, end)


@timeit
def part_2(blizzards, start_column, end_column, height, width):
    start = (-1, start_column)
    end = (height, end_column)

    total = find_best_path(blizzards, height, width, start, end)
    total = find_best_path(blizzards, height, width, end, start, total)
    total = find_best_path(blizzards, height, width, start, end, total)

    return total


def main():
    data = get_data()
    part_1(*data)
    part_2(*data)


if __name__ == "__main__":
    main()
