import hashlib
from itertools import islice

from utils import timeit


def gen_hashes(seed, prefix='00000'):
    index = 0
    while True:
        code = hashlib.md5(seed + bytes(f"{index}", encoding='utf-8')).hexdigest()
        if code.startswith(prefix):
            yield code
        index += 1


@timeit
def part_1(data):
    return ''.join(code[5] for code in islice(gen_hashes(bytes(data, encoding='utf-8')), 8))


@timeit
def part_2(data):
    password = ['_'] * 8
    print(''.join(password))

    for code in gen_hashes(bytes(data, encoding='utf-8')):
        if '0' <= code[5] <= '7':
            pos = int(code[5])
            if password[pos] == '_':
                password[pos] = code[6]
                print(''.join(password))
                if '_' not in password:
                    return password


def main():
    data = 'ugkcyxxp'
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
