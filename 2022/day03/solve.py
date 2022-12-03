from utils import timeit
from string import ascii_letters


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


def get_priority(snack):
    return 1 + ascii_letters.index(snack)


@timeit
def part_1(data):
    shared_snacks = [set(snacks[:len(snacks) // 2]) & set(snacks[len(snacks) // 2:]) for snacks in data]
    return sum(sum(map(get_priority, snacks)) for snacks in shared_snacks)


@timeit
def part_2(data):
    badges = [set(elf_1) & set(elf_2) & set(elf_3)
              for elf_1, elf_2, elf_3 in zip(data[0::3], data[1::3], data[2::3])]
    return sum(sum(map(get_priority, snacks)) for snacks in badges)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
