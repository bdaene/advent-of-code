from euclide import inv_mod
from math import gcd
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

    loop, key = 0, 1
    while key != key_b:
        key = (seed * key) % mod
        loop += 1

    print(loop)
    return pow(key_a, loop, 20201227)


def pollard_rho_log(alpha, beta, mod):
    """Tries to solve pow(alpha, x, mod) == beta for prime mod."""

    phi = mod - 1

    def get_new(x, a, b):
        """x == alpha**a * beta**b"""
        x3 = x % 3
        if x3 == 0:
            return (x * x) % mod, (2 * a) % phi, (2 * b) % phi
        elif x3 == 1:
            return (x * alpha) % mod, (a + 1) % phi, b
        else:
            return (x * beta) % mod, a, (b + 1) % phi

    x_t, a_t, b_t = 1, 0, 0
    x_h, a_h, b_h = get_new(x_t, a_t, b_t)

    while x_h != x_t:
        x_t, a_t, b_t = get_new(x_t, a_t, b_t)
        x_h, a_h, b_h = get_new(x_h, a_h, b_h)
        x_h, a_h, b_h = get_new(x_h, a_h, b_h)

    db = (b_h - b_t) % phi
    da = (a_t - a_h) % phi
    d = gcd(phi, gcd(db, da))
    db //= d
    da //= d
    phi //= d

    inv_db = inv_mod(db, phi)
    if inv_db is None:
        return None

    gamma = inv_db * da % phi
    for _ in range(d):
        if beta == pow(alpha, gamma, mod):
            return gamma
        gamma += phi

    return gamma


@timeit
def part_1_fast(keys, seed=7, mod=20201227):
    key_a, key_b = keys
    loop_b = pollard_rho_log(seed, key_b, mod)
    return pow(key_a, loop_b, mod)


def main():
    keys = get_keys()
    part_1(keys)
    part_1_fast(keys)


if __name__ == "__main__":
    main()
