from dataclasses import dataclass

from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            direction, steps = line.split()
            data.append((direction, int(steps)))
    return tuple(data)


DIRECTIONS = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
}


@dataclass
class Knot:
    x: int = 0
    y: int = 0

    def move(self, direction):
        dx, dy = direction
        self.x += dx
        self.y += dy

    def follow(self, knot):
        if abs(self.x - knot.x) > 1 or abs(self.y - knot.y) > 1:
            dx = (knot.x > self.x) - (knot.x < self.x)
            dy = (knot.y > self.y) - (knot.y < self.y)
            self.move((dx, dy))

    @property
    def position(self):
        return self.x, self.y


class Rope:

    def __init__(self, length):
        self.knots = tuple(Knot() for _ in range(length))

    def move_head(self, direction):
        self.knots[0].move(direction)
        for head, tail in zip(self.knots, self.knots[1:]):
            tail.follow(head)

    @property
    def tail(self):
        return self.knots[-1]


@timeit
def part_1(data, length=2):
    rope = Rope(length)
    visited = set()
    for direction, steps in data:
        for step in range(steps):
            rope.move_head(DIRECTIONS[direction])
            visited.add(rope.tail.position)

    return len(visited)


@timeit
def part_2(data):
    return part_1.func(data, length=10)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
