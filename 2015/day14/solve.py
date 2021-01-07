import re

from utils import timeit


@timeit
def get_data():
    data = {}
    pattern = re.compile(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')
    with open('input.txt') as input_file:
        for line in input_file:
            reindeer, speed, endurance, resting = pattern.match(line).groups()
            data[reindeer] = (int(speed), int(endurance), int(resting))
    return data


@timeit
def part_1(data, duration=2503):
    best = 0
    for reindeer, (speed, endurance, resting) in data.items():
        a, b = divmod(duration, endurance + resting)
        best = max(best, a * endurance * speed + min(b, endurance) * speed)

    return best


@timeit
def part_2(data, duration=2503):
    position = {reindeer: 0 for reindeer in data}
    points = {reindeer: 0 for reindeer in data}

    for t in range(1, duration + 1):
        for reindeer, (speed, endurance, resting) in data.items():
            a, b = divmod(t, endurance + resting)
            position[reindeer] = a * endurance * speed + min(b, endurance) * speed

        best = max(position.values())
        for reindeer in data:
            if position[reindeer] == best:
                points[reindeer] += 1

    return max(points.values())


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
