
import re


PATTERN = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')


def sign(x):
    return (x > 0) - (x < 0)


class Vector3:
    def __init__(self, x=0, y=0 ,z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iter__(self):
        def iter_func():
            yield self.x
            yield self.y
            yield self.z

        return iter_func()

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


def solve(moons, steps):
    periods = []
    for coord in range(3):
        xs = [moon[coord] for moon in moons]
        vs = [0] * len(moons)
        state = (tuple(xs), tuple(vs))
        states = {}

        steps = 0
        while state not in states:
            states[state] = steps
            for i, x in enumerate(xs):
                vs[i] += sum(sign(y-x) for y in xs)
            for i, v in enumerate(vs):
                xs[i] += v
            state = (tuple(xs), tuple(vs))
            steps += 1

        periods.append((steps - states[state], states[state]))

    print(periods)
    p = 1
    for period, start in periods:
        p *= period // gcd(p, period)

    return p


def gcd(a, b):
    while a:
        a, b = b%a, a
    return b


if __name__ == "__main__":
    moons = []
    with open('input.txt', 'r') as input_file:
        for line in input_file:
            x, y, z = map(int, PATTERN.match(line).groups())
            moons.append((x, y, z))
    print(solve(moons, 1000))

