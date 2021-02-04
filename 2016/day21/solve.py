import re
from itertools import permutations
from utils import timeit


@timeit
def get_data():
    data = []

    move_pattern = re.compile(r'move position (\d+) to position (\d+)')
    swap_pattern = re.compile(r'swap (position|letter) (\w+) with (position|letter) (\w+)')
    reverse_pattern = re.compile(r'reverse positions (\d+) through (\d+)')
    rotate_pattern = re.compile(r'rotate (left|right) (\d+) steps?')
    rotate_letter_pattern = re.compile(r'rotate based on position of letter (\w)')

    with open('input.txt') as input_file:
        for line in input_file:
            if match := move_pattern.match(line):
                a, b = match.groups()
                data.append(('move', int(a), int(b)))
            elif match := swap_pattern.match(line):
                a, b, c, d = match.groups()
                assert a == c
                if a == 'position':
                    b, d = int(b), int(d)
                data.append(('swap', a, b, d))
            elif match := reverse_pattern.match(line):
                a, b = match.groups()
                data.append(('reverse', int(a), int(b)+1))
            elif match := rotate_pattern.match(line):
                a, b = match.groups()
                data.append(('rotate', a, int(b)))
            elif match := rotate_letter_pattern.match(line):
                a = match.group(1)
                data.append(('rotate', 'letter', a))
            else:
                raise ValueError(f"Unknown operation {line}.")
    return data


@timeit
def part_1(data, password='abcdefgh'):

    password = list(password)

    for instruction, *values in data:
        if instruction == 'move':
            a, b = values
            c = password.pop(a)
            password.insert(b, c)
        elif instruction == 'reverse':
            a, b = values
            password = password[:a] + password[a:b][::-1] + password[b:]
        elif instruction == 'swap':
            a, b, c = values
            if a == 'letter':
                b = password.index(b)
                c = password.index(c)
            password[b], password[c] = password[c], password[b]
        elif instruction == 'rotate':
            a, b = values
            if a == 'letter':
                b = password.index(b)
                password = password[-1:] + password[:-1]
                password = password[-b:] + password[:-b]
                if b >= 4:
                    password = password[-1:] + password[:-1]
            elif a == 'left':
                password = password[b:] + password[:b]
            elif a == 'right':
                password = password[-b:] + password[:-b]
    return ''.join(password)


@timeit
def part_2(data, target='fbgdceah'):

    for password in permutations('abcdefgh'):
        scrambled_password = part_1.func(data, password)
        if scrambled_password == target:
            return ''.join(password)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
