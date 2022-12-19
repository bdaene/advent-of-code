import re
from itertools import accumulate, islice
from typing import NamedTuple

from utils import timeit

RESOURCES = ('ore', 'clay', 'obsidian')


class ResourceCount(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0

    def __lt__(self, other):
        return any(x < y for x, y in zip(self, other))

    def __le__(self, other):
        return all(x <= y for x, y in zip(self, other))

    def __add__(self, other):
        return ResourceCount(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        return ResourceCount(*(x - y for x, y in zip(self, other)))


@timeit
def get_data():
    data = {}
    with open('input.txt') as input_file:
        for line in input_file:
            blueprint, robots = line.split(':')
            blueprint_id = int(re.match(r'Blueprint (\d+)', blueprint).group(1))
            robot_costs = {}
            for robot in robots.strip()[:-1].split('.'):
                robot_name, cost = re.match(r'Each (\w+) robot costs (\d+ \w+(?: and \d+ \w+)?)',
                                            robot.strip()).groups()
                robot_costs[robot_name] = ResourceCount(**{resource: int(quantity)
                                                           for quantity, resource in
                                                           (re.match(r'(\d+) (\w+)', c).groups()
                                                            for c in cost.split(' and '))
                                                           })
            data[blueprint_id] = robot_costs
    return data


def get_max_geodes(blueprint, time_limit, start_resources, start_robots):
    max_robots_needed = ResourceCount(*map(max, zip(*blueprint.values())))
    geode_limit = list(accumulate(range(time_limit)))
    best = 0
    time_limit -= 1

    stack = [(0, 0, start_resources, start_robots)]

    while stack:
        time, geodes, resources, robots = stack.pop()
        best = max(best, geodes)

        if robots.ore < max_robots_needed.ore:
            needed_time, current_resources = time, resources
            while needed_time < time_limit and current_resources < blueprint['ore']:
                needed_time += 1
                current_resources += robots

            if needed_time < time_limit and geodes + geode_limit[time_limit - needed_time] > best:
                stack.append((needed_time + 1, geodes, current_resources - blueprint['ore'] + robots,
                              robots + ResourceCount(ore=1)))

        if robots.clay < max_robots_needed.clay and robots.ore > 0:
            needed_time, current_resources = time, resources
            while needed_time < time_limit and current_resources < blueprint['clay']:
                needed_time += 1
                current_resources += robots

            if needed_time < time_limit and geodes + geode_limit[time_limit - needed_time] > best:
                stack.append((needed_time + 1, geodes, current_resources - blueprint['clay'] + robots,
                              robots + ResourceCount(clay=1)))

        if robots.obsidian < max_robots_needed.obsidian and robots.clay > 0:
            needed_time, current_resources = time, resources
            while needed_time < time_limit and current_resources < blueprint['obsidian']:
                needed_time += 1
                current_resources += robots

            if needed_time < time_limit and geodes + geode_limit[time_limit - needed_time] > best:
                stack.append((needed_time + 1, geodes, current_resources - blueprint['obsidian'] + robots,
                              robots + ResourceCount(obsidian=1)))

        if robots.obsidian > 0:
            needed_time, current_resources = time, resources
            while needed_time < time_limit and current_resources < blueprint['geode']:
                needed_time += 1
                current_resources += robots

            if needed_time < time_limit and geodes + geode_limit[time_limit - needed_time] > best:
                stack.append((needed_time + 1, geodes + time_limit - needed_time,
                              current_resources - blueprint['geode'] + robots, robots))

    return best


@timeit
def part_1(data, time_limit=24):
    total = 0
    for blueprint_id, blueprint in data.items():
        geodes = get_max_geodes(blueprint, time_limit, ResourceCount(), ResourceCount(ore=1))
        print(blueprint_id, geodes)
        total += blueprint_id * geodes
    return total


@timeit
def part_2(data, time_limit=32):
    total = 1
    for blueprint_id, blueprint in islice(data.items(), 3):
        geodes = get_max_geodes(blueprint, time_limit, ResourceCount(), ResourceCount(ore=1))
        print(blueprint_id, geodes)
        total *= geodes
    return total


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
