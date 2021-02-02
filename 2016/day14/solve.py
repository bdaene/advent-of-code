import hashlib
import re
from collections import deque
from utils import timeit


def gen_hashes(seed, stretch):
    index = 0
    while True:
        code = hashlib.md5(seed + bytes(f"{index}", encoding='utf-8')).hexdigest()
        for _ in range(stretch):
            code = hashlib.md5(bytes(code, encoding='utf-8')).hexdigest()
        yield code
        index += 1


@timeit
def part_1(data, stretch=0):

    repeat_3 = re.compile(r'(\w)\1\1')

    keys = deque()
    valid_keys = []
    for i, code in enumerate(gen_hashes(data, stretch)):

        if match := repeat_3.search(code):
            c = match.group(1)
            keys.append((i, c, code))
            while keys[0][0] < i - 1000:
                key = keys.popleft()
                cs = key[1]*5
                for key_ in keys:
                    if key_[0] > key[0] + 1000:
                        break
                    if cs in key_[2]:
                        print(key, key_)
                        valid_keys.append(key)
                        if len(valid_keys) == 64:
                            return valid_keys[-1][0]


@timeit
def part_2(data):
    return part_1.func(data, stretch=2016)


def main():
    data = b'yjdafjpo'
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
