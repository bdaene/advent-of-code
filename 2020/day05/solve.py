from utils import timeit


@timeit
def part_1(seats):
    return max(seat_id for row, col, seat_id in seats)


@timeit
def part_2(seats):
    seat_ids = sorted(seat_id for row, col, seat_id in seats)
    for i, seat_id in enumerate(seat_ids[1:], 1):
        if seat_ids[i - 1] != seat_id - 1:
            return seat_id - 1


@timeit
def scan_seats(input_file):
    seats = []
    for line in input_file:
        line = line.replace('F', '0')
        line = line.replace('B', '1')
        line = line.replace('L', '0')
        line = line.replace('R', '1')
        seats.append((int(line[:7], 2), int(line[7:], 2), int(line, 2)))
    return seats


def main():
    with open('input.txt') as input_file:
        seats = scan_seats(input_file)

    part_1(seats)
    part_2(seats)


if __name__ == "__main__":
    main()
