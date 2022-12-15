import re
from itertools import combinations
from typing import NamedTuple

from matplotlib import pyplot
from utils import timeit


class Point(NamedTuple):
    x: int
    y: int

    def get_distance(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)

    def get_corners(self, radius):
        return (
            Point(self.x - radius, self.y),
            Point(self.x, self.y - radius),
            Point(self.x + radius, self.y),
            Point(self.x, self.y + radius),
        )


class Sensor(NamedTuple):
    position: Point
    radius: int


@timeit
def get_data():
    sensors, beacons = set(), set()
    pattern = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')
    with open('input.txt') as input_file:
        for line in input_file:
            sx, sy, bx, by = map(int, pattern.fullmatch(line.strip()).groups())
            beacon = Point(bx, by)
            sensor_position = Point(sx, sy)
            sensor = Sensor(sensor_position, sensor_position.get_distance(beacon))

            beacons.add(beacon)
            sensors.add(sensor)

    return frozenset(sensors), frozenset(beacons)


def show(sensors, beacons):
    pyplot.plot([sensor.position.x for sensor in sensors], [sensor.position.y for sensor in sensors], '*')
    pyplot.plot([beacon.x for beacon in beacons], [beacon.y for beacon in beacons], '+')

    for sensor in sensors:
        corners = sensor.position.get_corners(sensor.radius)
        corners += corners[:1]
        pyplot.fill(*zip(*corners), 'r-')
        pyplot.plot(*zip(*corners), 'b-')

    pyplot.show()


def get_impossible_ranges(sensors, y):
    impossible_ranges = []
    for sensor in sensors:
        delta = sensor.radius - abs(y - sensor.position.y)
        if delta < 0:
            continue
        impossible_ranges.append((sensor.position.x - delta, sensor.position.x + delta))
    return impossible_ranges


def get_gaps(ranges):
    gaps = []
    if not ranges:
        return gaps

    ranges.sort()
    end = ranges[0][0] - 1
    for left, right in ranges:
        if left > end + 1:
            gaps.append((end + 1, left - 1))
        end = max(end, right)

    return gaps


@timeit
def part_1(sensors, beacons, y=2000000):
    impossible_ranges = get_impossible_ranges(sensors, y)
    objects_on_line = set(sensor.position.x for sensor in sensors if sensor.position.y == y)
    objects_on_line |= set(beacon.x for beacon in beacons if beacon.y == y)

    gaps = get_gaps(impossible_ranges)

    return (max(right for left, right in impossible_ranges) - min(left for left, right in impossible_ranges) + 1
            - sum(right - left + 1 for left, right in gaps)
            - len(objects_on_line)
            )


def get_common_border(sensor_a: Sensor, sensor_b: Sensor):
    if sensor_a.position.get_distance(sensor_b.position) != sensor_a.radius + sensor_b.radius + 2:
        return None

    ax, bx = min(sensor_a.position.x, sensor_b.position.x), max(sensor_a.position.x, sensor_b.position.x)
    ay, by = min(sensor_a.position.y, sensor_b.position.y), max(sensor_a.position.y, sensor_b.position.y)
    corners = {corner
               for corner in (sensor_a.position.get_corners(sensor_a.radius + 1)
                              + sensor_b.position.get_corners(sensor_b.radius + 1))
               if ax <= corner.x <= bx and ay <= corner.y <= by}

    return tuple(sorted(corners))


def get_intersection(border_a, border_b):
    if border_a[1].y - border_a[0].y != border_a[1].x - border_a[0].x:
        border_a, border_b = border_b, border_a
    if border_b[1].y - border_b[0].y == border_b[1].x - border_b[0].x:
        return None  # borders are parallel

    x = (border_b[0].y - border_a[0].y + border_a[0].x + border_b[0].x) // 2
    y = (border_b[0].x - border_a[0].x + border_a[0].y + border_b[0].y) // 2

    if border_a[0].x <= x <= border_a[1].x and border_b[0].x <= x <= border_b[1].x:
        return Point(x, y)


@timeit
def part_2(sensors):
    borders = set()
    for sensor_a, sensor_b in combinations(sensors, 2):
        if sensor_a.position.get_distance(sensor_b.position) == sensor_a.radius + sensor_b.radius + 2:
            if border := get_common_border(sensor_a, sensor_b):
                # print(border)
                borders.add(border)
                # pyplot.plot(*zip(*border), '-g')

    positions = set()
    for border_a, border_b in combinations(borders, 2):
        if intersection := get_intersection(border_a, border_b):
            if all(sensor.position.get_distance(intersection) > sensor.radius for sensor in sensors):
                positions.add(intersection)

    # print(positions)
    position = positions.pop()
    # pyplot.plot([position.x], [position.y], 'om')
    return position.x * 4000000 + position.y


def main():
    sensors, beacons = get_data()
    part_1(sensors, beacons)
    part_2(sensors)
    # show(sensors, beacons)


if __name__ == "__main__":
    main()
