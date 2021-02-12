from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return input_file.readline().strip()


def remove_exclamation(stream):
    for c in stream:
        if c == '!':
            next(stream)
        else:
            yield c


def remove_garbage(stream):
    for c in stream:
        if c == '<':
            while c != '>':
                c = next(stream)
        else:
            yield c


@timeit
def part_1(data):

    stream = ''.join(remove_garbage(remove_exclamation(iter(data))))

    total = 0
    level = 0
    for c in stream:
        if c == '{':
            level += 1
            total += level
        elif c == '}':
            level -= 1

    return total


@timeit
def part_2(data):

    stream = remove_exclamation(iter(data))
    total = 0
    for c in stream:
        if c == '<':
            while c != '>':
                c = next(stream)
                total += 1
            total -= 1

    return total


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
