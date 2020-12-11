from collections import defaultdict, Counter
from itertools import product
from time import perf_counter


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


def main():
    seats = get_seats()
    part_1(seats)
    part_2(seats)


if __name__ == "__main__":
    main()
