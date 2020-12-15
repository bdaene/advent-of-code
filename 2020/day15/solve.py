from time import perf_counter


def timeit(func):
    def wrapper(*args, **kwargs):
        clock = perf_counter()
        result = func(*args, **kwargs)
        print(f"Execution of {func.__name__} took {(perf_counter() - clock) * 1000:.3f}ms.")
        print(f"Result: {result}")
        return result

    wrapper.func = func
    return wrapper


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
