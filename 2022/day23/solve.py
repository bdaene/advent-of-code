from collections import defaultdict

from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


def get_limits(elves):
    min_row, max_row = min(row for row, column in elves), max(row for row, column in elves)
    min_column, max_column = min(column for row, column in elves), max(column for row, column in elves)

    return (min_row, min_column), (max_row, max_column)


def show_elves(elves):
    (min_row, min_column), (max_row, max_column) = get_limits(elves)

    print("\n".join("".join("#" if (row, column) in elves else "."
                            for column in range(min_column, max_column + 1))
                    for row in range(min_row, max_row + 1))
          )


@timeit
def part_1(data, rounds=10):
    elves = {(row, column) for row, line in enumerate(data) for column, cell in enumerate(line) if cell == '#'}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    all_directions = {(r + c, c - r) for r, c in directions} | set(directions)
    directions = [((r, c), (r - c, c + r), (r + c, c - r)) for r, c in directions]

    # show_elves(elves)

    r = 0
    while r != rounds:
        proposed = defaultdict(set)

        for elf in elves:
            row, column = elf
            adjacent_elves = {cell for cell in ((row + r, column + c) for r, c in all_directions)
                              if cell in elves}
            if not adjacent_elves:
                continue

            for side in directions:
                if not any((row + r, column + c) in adjacent_elves for r, c in side):
                    proposed[(row + side[0][0], column + side[0][1])].add(elf)
                    break

        moved = False
        for proposition, proposing_elves in proposed.items():
            if len(proposing_elves) == 1:
                elf = proposing_elves.pop()
                elves.remove(elf)
                elves.add(proposition)
                moved = True

        r += 1
        # print(r)
        # show_elves(elves)
        directions = directions[1:] + directions[:1]

        if not moved:
            break

    (min_row, min_column), (max_row, max_column) = get_limits(elves)
    return r, (max_row - min_row + 1) * (max_column - min_column + 1) - len(elves)


@timeit
def part_2(data):
    return part_1.func(data, rounds=-1)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
