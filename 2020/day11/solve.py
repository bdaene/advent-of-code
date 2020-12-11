from collections import defaultdict, Counter
from itertools import product
from time import perf_counter

import numpy


def timeit(func):
    def wrapper(*args, **kwargs):
        clock = perf_counter()
        result = func(*args, **kwargs)
        print(f"Execution of {func.__name__} took {(perf_counter() - clock) * 1000:.3f}ms.")
        print(f"Result: {result}")
        return result

    return wrapper


@timeit
def get_seats():
    with open('input.txt') as input_file:
        return tuple(line.strip() for line in input_file)


def show_seats(seats):
    print('\n'.join(''.join(seats[(r, c)] for c in range(-1, 98)) for r in range(-1, 98)))


directions = ((-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1))


@timeit
def part_1(seats):
    nb_rows, nb_cols = len(seats), len(seats[0])
    seats_ = defaultdict(lambda: '.')
    for r, row in enumerate(seats):
        for c, seat in enumerate(row):
            if seat == 'L':
                seats_[(r, c)] = 'L'
    seats = seats_
    changed_seats = True

    def get_count(seat):
        count = 0
        r, c = seat
        for dr, dc in directions:
            if seats[(r + dr, c + dc)] == '#':
                count += 1
        return count

    while changed_seats:
        calculated_seats = {}
        for seat in product(range(0, nb_rows), range(0, nb_cols)):
            if seats[seat] == '.':
                continue
            calculated_seats[seat] = get_count(seat)

        changed_seats = False
        for seat, count in calculated_seats.items():
            if seats[seat] == 'L':
                if count == 0:
                    seats[seat] = '#'
                    changed_seats = True
            elif seats[seat] == '#':
                if count >= 4:
                    seats[seat] = 'L'
                    changed_seats = True
            else:
                raise RuntimeError(f"Calculated floor on {seat} : {seats[seat]=}")

        # show_seats(seats)

    return Counter(seats.values())['#']


@timeit
def part_2(seats):
    nb_rows, nb_cols = len(seats), len(seats[0])
    seats_ = defaultdict(lambda: '.')
    changed_seats = set()
    for r, row in enumerate(seats):
        for c, seat in enumerate(row):
            if seat == 'L':
                seats_[(r, c)] = 'L'
                changed_seats.add((r, c))
    seats = seats_
    changed_seats = True

    def get_count(seat):
        count = 0
        for dr, dc in directions:
            r, c = seat
            r += dr
            c += dc
            while 0 <= r < nb_rows and 0 <= c <= nb_cols:
                if seats[(r, c)] == '#':
                    count += 1
                    break
                elif seats[(r, c)] == 'L':
                    break
                r += dr
                c += dc
        return count

    while changed_seats:
        calculated_seats = {}
        for seat in product(range(0, nb_rows), range(0, nb_cols)):
            if seats[seat] == '.':
                continue
            calculated_seats[seat] = get_count(seat)

        changed_seats = False
        for seat, count in calculated_seats.items():
            if seats[seat] == 'L':
                if count == 0:
                    seats[seat] = '#'
                    changed_seats = True
            elif seats[seat] == '#':
                if count >= 5:
                    seats[seat] = 'L'
                    changed_seats = True
            else:
                raise RuntimeError(f"Calculated floor on {seat} : {seats[seat]=}")

        # show_seats(seats)

    return Counter(seats.values())['#']


@timeit
def part_2_bis(seats):
    rows = range(0, len(seats))
    cols = range(0, len(seats[0]))
    seats = {(row, col): False for row, col in product(rows, cols) if seats[row][col] == 'L'}

    def get_neighbors(row, col):
        neighbors = set()
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while r in rows and c in cols and (r, c) not in seats:
                r += dr
                c += dc
            if r in rows and c in cols:
                neighbors.add((r, c))
        return frozenset(neighbors)

    neighbors = {seat: get_neighbors(*seat) for seat in seats}
    # print(neighbors)
    seats_to_verify = seats

    def show():
        print('\n'.join(''.join(('#' if seats[(row, col)] else 'L') if (row, col) in seats else '.'
                                for col in cols)
                        for row in rows))
        print(seats_to_verify)

    # show()

    while seats_to_verify:
        calculated_seats = {seat: sum(1 for neighbor in neighbors[seat] if seats[neighbor]) for seat in
                            seats_to_verify}

        seats_to_verify = set()
        for seat, count in calculated_seats.items():
            if seats[seat]:
                if count >= 5:
                    seats[seat] = False
                    seats_to_verify |= neighbors[seat]
            else:
                if count == 0:
                    seats[seat] = True
                    seats_to_verify |= neighbors[seat]

        # show()

    return sum(1 for seat in seats if seats[seat])


@timeit
def part_1_bis(seats):
    seats = list(list(row) for row in seats)
    seats = (numpy.array(seats) == 'L')

    occupied_seats = numpy.zeros(seats.shape, dtype=bool)

    while True:
        count = numpy.zeros(seats.shape, dtype=int)
        count[:-1, :-1] += occupied_seats[1:, 1:]
        count[:-1, 1:] += occupied_seats[1:, :-1]
        count[1:, :-1] += occupied_seats[:-1, 1:]
        count[1:, 1:] += occupied_seats[:-1, :-1]
        count[:, :-1] += occupied_seats[:, 1:]
        count[:, 1:] += occupied_seats[:, :-1]
        count[1:, :] += occupied_seats[:-1, :]
        count[:-1, :] += occupied_seats[1:, :]

        occupied_seats_ = seats & ((occupied_seats & (count < 4)) | ~occupied_seats & (count == 0))
        if (occupied_seats_ == occupied_seats).all():
            break
        occupied_seats = occupied_seats_

    return occupied_seats.sum()


def main():
    seats = get_seats()
    part_1_bis(seats)
    # part_1(seats)
    # part_2(seats)
    part_2_bis(seats)


if __name__ == "__main__":
    main()
