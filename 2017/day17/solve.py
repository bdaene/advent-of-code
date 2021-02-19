from collections import deque
from utils import timeit


@timeit
def part_1(data):
    state = deque([0])
    for i in range(1, 2018):
        state.rotate(-data)
        state.append(i)

    return state[0]


@timeit
def part_2(data):
    state = deque([0])
    for i in range(1, 50000001):
        state.rotate(-data)
        state.append(i)

    while state[-1] != 0:
        state.rotate(1)
    return state[0]


@timeit
def part_2_bis(data):
    current_pos = 1
    value_at_1 = None

    for i in range(1, 50000001):
        current_pos = (current_pos + data) % i + 1
        if current_pos == 1:
            value_at_1 = i
    return value_at_1


def main():
    data = 356
    part_1(data)
    # part_2(data)
    part_2_bis(data)


if __name__ == "__main__":
    main()
