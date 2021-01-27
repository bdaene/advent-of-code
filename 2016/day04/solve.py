import re
from collections import Counter
from utils import timeit


@timeit
def get_data():
    data = []
    pattern = re.compile(r'([a-z-]*)-(\d+)\[([a-z]{5})\]')
    with open('input.txt') as input_file:
        for line in input_file:
            name, sector, checksum = pattern.fullmatch(line.strip()).groups()
            data.append((name, int(sector), checksum))
    return data


def is_real_room(name, checksum):
    count = Counter(name)
    del count['-']
    return checksum == ''.join(sorted(count, key=lambda c: (-count[c], c))[:5])


@timeit
def part_1(data):
    return sum(sector for name, sector, checksum in data if is_real_room(name, checksum))


def decrypt(name, sector):
    return ''.join(' ' if c == '-' else chr((ord(c) - ord('a') + sector)%26 + ord('a')) for c in name)


@timeit
def part_2(data):
    for name, sector, checksum in data:
        if is_real_room(name, checksum):
            decrypted_name = decrypt(name, sector)
            if all(word in decrypted_name for word in ('north', 'pole', 'object')):
                print(f"{sector:6}: {decrypt(name, sector)}")
                return sector


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
