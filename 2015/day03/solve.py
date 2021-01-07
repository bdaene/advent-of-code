from collections import Counter

from utils import timeit


@timeit
def get_moves():
    with open('input.txt') as input_file:
        return input_file.readline().strip()


@timeit
def part_1(moves):
    x, y = 0, 0
    houses = Counter()
    houses[(x, y)] = 1

    for move in moves:
        if move == '^':
            y += 1
        elif move == 'v':
            y -= 1
        elif move == '>':
            x += 1
        elif move == '<':
            x -= 1
        houses[(x, y)] += 1

    return len(houses)


@timeit
def part_2(moves):
    santas = [0, 0]
    houses = Counter({santa: 1 for santa in santas})

    santa = 0
    for move in moves:
        if move == '^':
            santas[santa] += 1j
        elif move == 'v':
            santas[santa] -= 1j
        elif move == '>':
            santas[santa] += 1
        elif move == '<':
            santas[santa] -= 1
        houses[santas[santa]] += 1
        santa += 1
        santa %= len(santas)

    return len(houses)


def main():
    moves = get_moves()
    part_1(moves)
    part_2(moves)


if __name__ == "__main__":
    main()
