from utils import timeit


@timeit
def part_1(numbers=(15, 12, 0, 14, 3, 1), target=2020):
    seen = {}
    for i, n in enumerate(numbers[:-1]):
        seen[n] = i

    i = len(numbers) - 1
    prev = numbers[i]

    while i + 1 != target:
        if prev in seen:
            n = i - seen[prev]
        else:
            n = 0
        seen[prev] = i
        prev = n
        i += 1

    print(len(seen))
    return prev


@timeit
def part_2():
    return part_1.func(target=30000000)


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
