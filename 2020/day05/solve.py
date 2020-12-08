def part_1(seats):
    print(max(seat_id for row, col, seat_id in seats))


def part_2(seats):
    seat_ids = sorted(seat_id for row, col, seat_id in seats)
    for i, seat_id in enumerate(seat_ids[1:], 1):
        if seat_ids[i - 1] != seat_id - 1:
            print(seat_id - 1)


def scan_seats(input_file):
    for line in input_file:
        line = line.replace('F', '0')
        line = line.replace('B', '1')
        line = line.replace('L', '0')
        line = line.replace('R', '1')
        yield int(line[:7], 2), int(line[7:], 2), int(line, 2)


def main():
    with open('input.txt') as input_file:
        seats = list(scan_seats(input_file))

    print(seats)
    part_1(seats)
    part_2(seats)


if __name__ == "__main__":
    main()
