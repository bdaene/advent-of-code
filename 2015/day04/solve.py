from hashlib import md5

from utils import timeit


@timeit
def part_1(secret_key='yzbqklnj', nb_zeros=5):
    n = 0
    prefix = '0' * nb_zeros
    while not md5(f"{secret_key}{n}".encode()).hexdigest().startswith(prefix):
        n += 1

    return n


@timeit
def part_2():
    return part_1.func(nb_zeros=6)


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
