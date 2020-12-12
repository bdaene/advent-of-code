from cmath import rect, pi
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
def get_directions():
    directions = []
    with open('input.txt') as input_file:
        for line in input_file:
            action, value = line[0], int(line[1:])
            directions.append((action, value))
    return directions


@timeit
def part_1(directions):
    position = 0
    direction = 1

    for action, value in directions:
        if action == 'N':
            position += value * 1j
        elif action == 'S':
            position -= value * 1j
        elif action == 'E':
            position += value
        elif action == 'W':
            position -= value
        elif action == 'L':
            direction *= rect(1, value * pi / 180)
        elif action == 'R':
            direction *= rect(1, -value * pi / 180)
        elif action == 'F':
            position += direction * value

    return abs(position.real) + abs(position.imag)


@timeit
def part_2(directions):
    position = 0
    waypoint = 10 + 1j

    for action, value in directions:
        if action == 'N':
            waypoint += value * 1j
        elif action == 'S':
            waypoint -= value * 1j
        elif action == 'E':
            waypoint += value
        elif action == 'W':
            waypoint -= value
        elif action == 'L':
            waypoint *= rect(1, value * pi / 180)
        elif action == 'R':
            waypoint *= rect(1, -value * pi / 180)
        elif action == 'F':
            position += waypoint * value

    return abs(position.real) + abs(position.imag)


def main():
    directions = get_directions()
    part_1(directions)
    part_2(directions)


if __name__ == "__main__":
    main()
