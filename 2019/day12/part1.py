
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
        return f"({self.x:3}, {self.y:3}, {self.z:3})"

def solve(moons, steps):
    positions = [Vector3(*moon) for moon in moons]
    velocities = [Vector3() for moon in moons]
    print(f"{str(0): >6} {str(positions): >50} {str(velocities): >50}")

    for step in range(1, steps+1):
        for a, pos_a in enumerate(positions):
            for b, pos_b in enumerate(positions[a+1:], a+1):
                velocities[a] += Vector3(*map(sign, pos_b - pos_a))
                velocities[b] += Vector3(*map(sign, pos_a - pos_b))

        for a, pos_a in enumerate(positions):
            positions[a] += velocities[a]

        print(f"{str(step): >6} {str(positions): >50} {str(velocities): >50}")

    total = 0
    for pos, vel in zip(positions, velocities):
        total += sum(map(abs, pos)) * sum(map(abs, vel))

    return total


if __name__ == "__main__":
    moons = []
    with open('input.txt', 'r') as input_file:
        for line in input_file:
            x, y, z = map(int, PATTERN.match(line).groups())
            moons.append((x, y, z))
    print(solve(moons, 2772))

