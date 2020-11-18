
from itertools import product


def solve(start, end):
    count = 0
    for n in product(range(10), repeat=6):
        if any(n[k] > n[k+1] for k in range(5)):
            continue
        s = 0
        for d in n:
            s *= 10
            s += d
        if not (start <= s <= end):
            continue
        if any(n[k] == n[k+1] and (k == 0 or n[k-1] != n[k]) and (k == 4 or n[k+1] != n[k+2]) for k in range(5)):
            count += 1
    return count


if __name__ == "__main__":
    print(solve(125730, 579381))
