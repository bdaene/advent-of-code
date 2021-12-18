from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from utils import timeit


@dataclass
class Number:
    left: Optional[Number] = None
    right: Optional[Number] = None
    magnitude: Optional[int] = None

    def is_regular_number(self):
        return self.left is None and self.right is None

    @staticmethod
    def from_string(string):
        stack = []
        value = None
        for c in string:
            if c.isdigit():
                value = (0 if value is None else value * 10) + int(c)
            else:
                if value is not None:
                    stack.append(Number(magnitude=value))
                    value = None
                if c == ']':
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(Number(left, right))

        return stack.pop()

    def __str__(self):
        if self.is_regular_number():
            return f'{self.magnitude}'
        else :
            return f'[{self.left},{self.right}]'

    def __add__(self, other):
        total = Number(self, other)
        total.reduce()
        return total

    def reduce(self):
        updated = True
        while updated:
            self.explode()
            updated = self.split()

    def explode(self, depth=0, last_regular_number=None, carry=0):
        if self.is_regular_number():
            self.magnitude += carry
            return self, self, 0

        if depth >= 4:
            if last_regular_number is not None:
                last_regular_number.magnitude += self.left.magnitude + carry
            new_node = Number(magnitude=0)
            return new_node, new_node, self.right.magnitude
        else:
            depth += 1
            self.left, last_regular_number, carry = self.left.explode(depth, last_regular_number, carry)
            self.right, last_regular_number, carry = self.right.explode(depth, last_regular_number, carry)
            return self, last_regular_number, carry

    def split(self):
        assert not self.is_regular_number()

        if self.left.is_regular_number():
            if self.left.magnitude > 9:
                half_down = self.left.magnitude // 2
                self.left = Number(Number(magnitude=half_down), Number(magnitude=self.left.magnitude - half_down))
                return True
        elif self.left.split():
            return True

        if self.right.is_regular_number():
            if self.right.magnitude > 9:
                half_down = self.right.magnitude // 2
                self.right = Number(Number(magnitude=half_down), Number(magnitude=self.right.magnitude - half_down))
                return True
        elif self.right.split():
            return True

        return False

    def get_magnitude(self):
        if self.is_regular_number():
            return self.magnitude
        else:
            return 3*self.left.get_magnitude() + 2*self.right.get_magnitude()


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(line.strip() for line in input_file)


@timeit
def part_1(data):
    total = Number.from_string(data[0])
    for number in data[1:]:
        total += Number.from_string(number)

    print(total)
    return total.get_magnitude()


@timeit
def part_2(data):
    return max((Number.from_string(a) + Number.from_string(b)).get_magnitude()
               for a in data for b in data if a != b)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
