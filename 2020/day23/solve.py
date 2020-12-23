from utils import timeit


def play(cups, nb_cups, moves):
    next_cup = {a: b for a, b in zip(cups, cups[1:])}
    last_cup = cups[-1]
    for cup in range(len(cups) + 1, nb_cups + 1):
        next_cup[last_cup] = cup
        last_cup = cup
    next_cup[last_cup] = 1

    current_cup = cups[0]

    for _ in range(moves):
        a = next_cup[current_cup]
        b = next_cup[a]
        c = next_cup[b]
        next_cup[current_cup] = next_cup[c]

        dest_cup = current_cup - 1
        if dest_cup == 0:
            dest_cup = nb_cups
        while dest_cup in (a, b, c):
            dest_cup -= 1
            if dest_cup == 0:
                dest_cup = nb_cups

        next_cup[c] = next_cup[dest_cup]
        next_cup[dest_cup] = a

        current_cup = next_cup[current_cup]

    return next_cup


@timeit
def part_1(cups=(1, 5, 7, 6, 2, 3, 9, 8, 4), nb_cups=9, moves=100):
    next_cup = play(cups, nb_cups, moves)

    cup, cups = 1, []
    for _ in range(nb_cups - 1):
        cup = next_cup[cup]
        cups.append(cup)
    return ''.join(map(str, cups))


@timeit
def part_2(cups=(1, 5, 7, 6, 2, 3, 9, 8, 4), nb_cups=10 ** 6, moves=10 ** 7):
    next_cup = play(cups, nb_cups, moves)
    a = next_cup[1]
    b = next_cup[a]

    return a * b


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
