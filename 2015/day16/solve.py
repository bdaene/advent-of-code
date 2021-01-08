from operator import eq, gt, lt

from utils import timeit


@timeit
def get_aunts():
    aunts = []
    with open('input.txt') as input_file:
        for line in input_file:
            infos = [info.split(': ') for info in line[line.index(':') + 2:].split(', ')]
            aunts.append({name: int(value) for name, value in infos})
    return aunts


@timeit
def part_1(aunts):
    tape = {'children': 3,
            'cats': 7,
            'samoyeds': 2,
            'pomeranians': 3,
            'akitas': 0,
            'vizslas': 0,
            'goldfish': 5,
            'trees': 3,
            'cars': 2,
            'perfumes': 1,
            }

    for aunt, info in enumerate(aunts, 1):
        if all(tape[name] == value for name, value in info.items()):
            return aunt


@timeit
def part_2(aunts):
    tape = {'children': (eq, 3),
            'cats': (gt, 7),
            'samoyeds': (eq, 2),
            'pomeranians': (lt, 3),
            'akitas': (eq, 0),
            'vizslas': (eq, 0),
            'goldfish': (lt, 5),
            'trees': (gt, 3),
            'cars': (eq, 2),
            'perfumes': (eq, 1),
            }

    for aunt, info in enumerate(aunts, 1):
        if all(tape[name][0](value, tape[name][1]) for name, value in info.items()):
            return aunt


def main():
    aunts = get_aunts()
    part_1(aunts)
    part_2(aunts)


if __name__ == "__main__":
    main()
