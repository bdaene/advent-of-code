from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            data.append(line.strip())
    return data


@timeit
def part_1(data):
    return sum(1 for line in data if len(line.split()) == len(set(line.split())))


@timeit
def part_2(data):

    def is_valid(passphrase):
        words = list(map(tuple, map(sorted, passphrase.split())))
        return len(set(words)) == len(words)

    return sum(1 for passphrase in data if is_valid(passphrase))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
