import re
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


def contains_abba(string):
    for i in range(len(string) - 4 + 1):
        a, b = string[i], string[i+1]
        if a != b and string[i+2] == b and string[i+3] == a:
            return True
    return False


def split(address):
    sub_address = []
    i = 0
    for j, c in enumerate(address):
        if c in ('[', ']'):
            sub_address.append(address[i:j])
            i = j + 1
    sub_address.append(address[i:])

    return sub_address[::2], sub_address[1::2]


def is_tls(address):
    supernets, hypernets = split(address)

    return any(contains_abba(add) for add in supernets) and not any(contains_abba(add) for add in hypernets)


@timeit
def part_1(data):
    return sum(1 for address in data if is_tls(address))


def is_ssl(address):
    supernets, hypernets = split(address)

    for supernet in supernets:
        for i in range(len(supernet)-3+1):
            a, b, c = supernet[i:i+3]
            if a != b and a == c:
                if any(b+a+b in hypernet for hypernet in hypernets):
                    return True

    return False


@timeit
def part_2(data):
    return sum(1 for address in data if is_ssl(address))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
