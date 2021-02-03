from collections import deque
from utils import timeit


@timeit
def part_1(data):

    elves = deque(range(1, data+1))
    while len(elves) > 1:
        elves.rotate(-1)
        elves.popleft()

    return elves[0]


@timeit
def part_2(data):
    elves_left = {i: i+1 for i in range(1, data)}
    elves_left[data] = 1

    elves_right = {i: i-1 for i in range(2, data+1)}
    elves_right[1] = data

    current_elf = 1
    opposite_elf = data//2 + 1
    nb_elves = data
    while nb_elves > 1:
        elves_right[elves_left[opposite_elf]] = elves_right[opposite_elf]
        elves_left[elves_right[opposite_elf]] = elves_left[opposite_elf]
        current_elf = elves_left[current_elf]
        if nb_elves % 2 == 0:
            opposite_elf = elves_left[opposite_elf]
        else:
            opposite_elf = elves_left[elves_left[opposite_elf]]
        nb_elves -= 1

    return current_elf


def main():
    data = 3012210
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
