import re
from heapq import heappop, heappush
from itertools import chain
from random import random
from utils import timeit


@timeit
def get_data():
    data = {}
    pattern = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')
    with open('input.txt') as input_file:
        for line in input_file:
            if match := pattern.match(line):
                x, y, size, used, available, use = map(int, match.groups())
                assert used + available == size
                data[(x, y)] = (size, used, available)
    return data


@timeit
def part_1(data):

    used_values = sorted(used for size, used, available in data.values())
    available_values = sorted(available for size, used, available in data.values())

    i, j = 0, 0
    count = 0
    while i < len(used_values):
        used = used_values[i]
        if used > 0:
            while j < len(available_values) and available_values[j] < used:
                j += 1
            count += len(available_values) - j
        i += 1

    return count


@timeit
def part_2(data):

    grid = {node: used for node, (size, used, available) in data.items()}
    grid_size = {node: size for node, (size, used, available) in data.items()}
    max_x, max_y = max(x for x, y in grid), max(y for x, y in grid)

    def gen_moves_from(node, current_grid):
        used = current_grid[node]
        if used == 0:
            return
        x, y = node
        for (x_, y_) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= x_ <= max_x and 0 <= y_ <= max_y and used + current_grid[(x_, y_)] <= grid_size[(x_, y_)]:
                yield (x, y), (x_, y_)

    def gen_moves_to(node, current_grid):
        x, y = node
        for (x_, y_) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= x_ <= max_x and 0 <= y_ <= max_y:
                node_ = (x_, y_)
                used = current_grid[node_]
                if used > 0 and current_grid[node] + used <= grid_size[node]:
                    yield node_, node

    available_moves = frozenset(chain(*(gen_moves_from(node, grid) for node in grid)))
    pos_g = (max_x, 0)

    # state = (nb_moves + dist_g, pos_g, nb_moves, random, available_moves, grid)
    start = (0 + sum(pos_g), pos_g, 0, random(), available_moves, grid)
    heap = [start]
    seen = set()

    while heap:
        cost, pos_g, nb_moves, _, available_moves, grid = heappop(heap)
        if pos_g == (0, 0):
            return nb_moves

        for node_a, node_b in available_moves:
            grid_ = grid.copy()
            grid_[node_b] += grid_[node_a]
            grid_[node_a] = 0
            available_moves_ = frozenset(move for move in available_moves if node_a != move[0] and node_b not in move)
            available_moves_ |= frozenset(gen_moves_from(node_b, grid_))
            available_moves_ |= frozenset(gen_moves_to(node_a, grid_))
            pos_g_ = node_b if pos_g == node_a else pos_g
            key = (pos_g_, available_moves_)
            if key in seen:
                continue
            seen.add(key)
            state = (nb_moves + sum(pos_g_) + 1, pos_g_, nb_moves + 1, random(), available_moves_, grid_)
            heappush(heap, state)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
