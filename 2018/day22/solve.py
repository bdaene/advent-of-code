import re
from functools import cache
from heapq import heappush, heappop
from utils import timeit


@timeit
def get_data():
    depth_pattern = re.compile(r'depth: (\d+)')
    target_pattern = re.compile(r'target: (\d+,\d+)')
    with open('input.txt') as input_file:
        depth = int(depth_pattern.match(input_file.readline()).group(1))
        target = tuple(map(int, target_pattern.match(input_file.readline()).group(1).split(',')))
    return depth, target


@timeit
def part_1(data):
    depth, target = data

    @cache
    def get_geological_index(position):
        if position == (0, 0):
            return 0
        if position == target:
            return 0
        x, y = position
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271
        return get_erosion_level((x - 1, y)) * get_erosion_level((x, y - 1))

    def get_erosion_level(position):
        return (get_geological_index(position) + depth) % 20183

    return sum(get_erosion_level((x, y)) % 3 for x in range(target[0] + 1) for y in range(target[1] + 1))


@timeit
def part_2(data):
    depth, target = data

    @cache
    def get_geological_index(position):
        if position == (0, 0):
            return 0
        if position == target:
            return 0
        x_, y_ = position
        if y_ == 0:
            return x_ * 16807
        if x_ == 0:
            return y_ * 48271
        return get_erosion_level((x_ - 1, y_)) * get_erosion_level((x_, y_ - 1))

    def get_erosion_level(position):
        return (get_geological_index(position) + depth) % 20183

    tools = {
        0: {'climbing gear', 'torch'},
        1: {'climbing gear', ''},
        2: {'', 'torch'},
    }

    heap = [(0 + sum(target), 0, (0, 0), 'torch')]
    seen = set()
    while heap:
        _, time, (x, y), tool = heappop(heap)
        if (x, y) == target and tool == 'torch':
            return time
        if (x, y, tool) in seen:
            continue
        seen.add((x, y, tool))

        region = get_erosion_level((x, y)) % 3

        def push_move(time_, pos_, tool_):
            dist = abs(pos_[0] - target[0]) + abs(pos_[1] + target[1])
            heappush(heap, (time_ + dist, time_, pos_, tool_))

        # Switch tool
        other_tool = tuple(tools[region] - {tool})[0]
        push_move(time + 7, (x, y), other_tool)

        if x > 0 and tool in tools[get_erosion_level((x - 1, y)) % 3]:
            push_move(time + 1, (x - 1, y), tool)
        if y > 0 and tool in tools[get_erosion_level((x, y - 1)) % 3]:
            push_move(time + 1, (x, y - 1), tool)
        if tool in tools[get_erosion_level((x + 1, y)) % 3]:
            push_move(time + 1, (x + 1, y), tool)
        if tool in tools[get_erosion_level((x, y + 1)) % 3]:
            push_move(time + 1, (x, y + 1), tool)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
