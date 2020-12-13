from time import perf_counter

from euclide import solve_chinese_remainders


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
    with open('input.txt') as input_file:
        timestamp = int(input_file.readline())
        buses = input_file.readline().strip().split(',')
    return timestamp, buses


def get_time(timestamp, bus):
    time = timestamp % bus
    if time > 0:
        time = bus - time
    return time


@timeit
def part_1(data):
    timestamp, buses = data

    buses = list(int(bus) for bus in buses if bus != 'x')
    best, bus_id = max(buses), max(buses)
    for bus in buses:
        time = get_time(timestamp, bus)
        if time < best:
            best, bus_id = time, bus

    return best * bus_id


@timeit
def part_2(data):
    timestamp, buses = data

    remainders = [] if buses[0] == 'x' else [(0, int(buses[0]))]
    for i, bus in enumerate(buses[1:], 1):
        if bus != 'x':
            bus = int(bus)
            remainders.append((bus - i, bus))

    timestamp = solve_chinese_remainders(remainders)

    assert all(
        get_time(timestamp, int(bus)) % int(bus) == i % int(bus) for i, bus in enumerate(buses) if bus != 'x')
    print([bus if bus == 'x' else get_time(timestamp, int(bus)) for bus in buses])
    return timestamp


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
