from time import perf_counter


def timeit(func):
    def wrapper(*args, **kwargs):
        clock = perf_counter()
        result = func(*args, **kwargs)
        print(f"Execution of {func.__name__} took {(perf_counter() - clock) * 1000:.3f}ms.")
        print(f"Result: {result}")
        return result

    return wrapper


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


@timeit
def part_1(data):
    return len(data)


@timeit
def part_2(data):
    return len(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
