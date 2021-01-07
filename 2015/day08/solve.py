from utils import timeit


@timeit
def get_strings():
    strings = []
    with open('input.txt') as input_file:
        for line in input_file:
            strings.append(line.strip())
    return strings


@timeit
def part_1(strings):
    total = 0
    for string in strings:
        total += 2
        c = 1
        while c < len(string) - 1:
            if string[c] == '\\':
                c += 1
                total += 1
                if string[c] == 'x':
                    total += 2
                    c += 2
            c += 1

    return total


@timeit
def part_2(strings):
    total = 0
    for string in strings:
        total += 2
        for c in string:
            if c in ('"', '\\'):
                total += 1

    return total


def main():
    strings = get_strings()
    part_1(strings)
    part_2(strings)


if __name__ == "__main__":
    main()
