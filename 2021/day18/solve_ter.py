import json
from dataclasses import dataclass
from itertools import chain, permutations

from utils import timeit


@dataclass(frozen=True)
class Number:
    values: tuple[int, ...]
    depths: tuple[int, ...]

    @classmethod
    def from_string(cls, string):

        def extract(number, depth=0):
            if isinstance(number, int):
                return (number,), (depth,)
            else:
                left, right = number
                left_values, left_depths = extract(left, depth + 1)
                right_values, right_depths = extract(right, depth + 1)
                return left_values + right_values, left_depths + right_depths

        return cls(*extract(json.loads(string)))

    def __add__(self, other):
        values: list[int] = list(chain(self.values, other.values))
        depths: list[int] = list(depth + 1 for depth in chain(self.depths, other.depths))

        def explode():
            i = 0
            while i < len(values):
                if depths[i] > 4:
                    if i - 1 >= 0:
                        values[i - 1] += values[i]
                    if i + 2 < len(values):
                        values[i + 2] += values[i + 1]
                    del values[i + 1]
                    del depths[i + 1]
                    values[i] = 0
                    depths[i] -= 1
                i += 1

        def split():
            for i, (value, depth) in enumerate(zip(values, depths)):
                if value > 9:
                    half = value // 2
                    depths[i] = depth + 1
                    values[i] = value - half
                    depths.insert(i, depth + 1)
                    values.insert(i, half)
                    return True
            return False

        change = True
        while change:
            explode()
            change = split()

        return Number(tuple(values), tuple(depths))

    def magnitude(self):
        total, factor, stack = 0, 1, []
        for value, depth in zip(self.values, self.depths):
            while depth > len(stack):
                stack.append(False)
                factor *= 3
            total += value * factor
            while stack[-1] is True:
                stack.pop()
                if not stack:
                    return total
                factor //= 2
            stack[-1] = True
            factor //= 3
            factor *= 2


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(Number.from_string(line) for line in input_file)


@timeit
def part_1(data):
    total = data[0]
    for number in data[1:]:
        total += number

    print(total)
    return total.magnitude()


@timeit
def part_2(data):
    return max((a + b).magnitude() for a, b in permutations(data, 2))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
