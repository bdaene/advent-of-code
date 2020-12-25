from utils import timeit


@timeit
def get_keys():
    keys = []
    with open('input.txt') as input_file:
        for line in input_file:
            keys.append(int(line))
    return keys


@timeit
def part_1(keys, seed=7, mod=20201227):
    key_a, key_b = keys
    loop_a = loop_b = None

    loop, key = 0, 1
    while loop_a is None or loop_b is None:
        if key == key_a:
            loop_a = loop
        if key == key_b:
            loop_b = loop

        key *= seed
        key %= mod
        loop += 1

    print(loop_a, loop_b)
    return pow(7, loop_a * loop_b, 20201227)


@timeit
def part_2(keys):
    pass  # Nothing to do


def main():
    keys = get_keys()
    part_1(keys)
    part_2(keys)


if __name__ == "__main__":
    main()
