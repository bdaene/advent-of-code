import re
from copy import deepcopy

from utils import timeit


def parse_stacks(boat):
    columns = [i for i, c in enumerate(boat[-1]) if not c.isspace()]
    stacks = tuple([] for _ in columns)
    for row in reversed(boat[:-1]):
        for i, col in enumerate(columns):
            if not (crate := row[col]).isspace():
                stacks[i].append(crate)

    return stacks


@timeit
def get_data():
    with open('input.txt') as input_file:
        boat = []
        for line in input_file:
            if line.isspace():
                break
            else:
                boat.append(line)
        stacks = parse_stacks(boat)

        moves = []
        pattern = re.compile(r'move (\d+) from (\d) to (\d)')
        for line in input_file:
            crates, from_stack, to_stack = map(int, pattern.fullmatch(line.strip()).groups())
            moves.append((crates, from_stack - 1, to_stack - 1))
    return stacks, moves


@timeit
def part_1(stacks, moves):
    for crates, from_stack, to_stack in moves:
        stacks[to_stack].extend(stacks[from_stack][-crates:][::-1])
        del stacks[from_stack][-crates:]
    return ''.join(stack[-1] for stack in stacks)


@timeit
def part_2(stacks, moves):
    for crates, from_stack, to_stack in moves:
        stacks[to_stack].extend(stacks[from_stack][-crates:])
        del stacks[from_stack][-crates:]
    return ''.join(stack[-1] for stack in stacks)


def main():
    stacks, moves = get_data()
    part_1(deepcopy(stacks), moves)
    part_2(deepcopy(stacks), moves)


if __name__ == "__main__":
    main()
