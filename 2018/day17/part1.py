
import sys

import re
from collections import defaultdict

sys.setrecursionlimit(10000)


def solve(verticals, horizontals):
    min_y = min(min(horizontals), min(min(clay[0] for clay in vertical) for vertical in verticals.values()))
    max_y = max(max(horizontals), max(max(clay[0] for clay in vertical) for vertical in verticals.values()))

    min_x = min(min(verticals), min(min(clay[0] for clay in horizontal) for horizontal in horizontals.values())) - 1
    max_x = max(max(verticals), max(max(clay[0] for clay in horizontal) for horizontal in horizontals.values())) + 1

    min_x = min(min_x, 500)
    max_x = max(max_x, 500)

    print(min_x, max_x, min_y, max_y)

    grid = defaultdict(lambda: '.')
    grid[(500, 0)] = '+'

    def show_grid():
        print('\n'.join(''.join(grid[(x, y)] for x in range(min_x, max_x + 1)) for y in range(max_y + 1)))

    for x, vertical in verticals.items():
        for clay in vertical:
            for y in range(clay[0], clay[1]+1):
                grid[(x, y)] = '#'

    for y, horizontal in horizontals.items():
        for clay in horizontal:
            for x in range(clay[0], clay[1]+1):
                grid[(x, y)] = '#'

    def flood(x, y):
        assert(grid[(x, y)] == '.')
        grid[(x, y)] = '|'
        if y >= max_y or grid[(x, y + 1)] == '|' or (grid[(x, y + 1)] == '.' and not flood(x, y + 1)):
            return False

        xl = x - 1
        while grid[(xl, y)] == '.':
            grid[(xl, y)] = '|'
            if y >= max_y or grid[(xl, y + 1)] == '|' or (grid[(xl, y + 1)] == '.' and not flood(xl, y + 1)):
                break
            xl -= 1

        xr = x + 1
        while grid[(xr, y)] == '.':
            grid[(xr, y)] = '|'
            if y >= max_y or grid[(xr, y + 1)] == '|' or (grid[(xr, y + 1)] == '.' and not flood(xr, y + 1)):
                break
            xr += 1

        # show_grid()

        if grid[(xl, y)] == '#' and grid[(xr, y)] == '#':
            for x in range(xl + 1, xr):
                grid[(x, y)] = '~'
            return True
        else:
            return False

    flood(500, 1)

    show_grid()

    count_reached = sum(1 for y in range(min_y, max_y + 1) for x in range(min_x, max_x + 1) if grid[(x, y)] in '|~')
    print(f"{count_reached} tiles reached by water")

    count_water = sum(1 for y in range(min_y, max_y + 1) for x in range(min_x, max_x + 1) if grid[(x, y)] == '~')
    print(f"{count_water} tiles have water")

    return min_y, max_y, count_reached, count_water


PATTERN = re.compile(r'([xy])=(\d+), ([xy])=(\d+)..(\d+)')

if __name__ == "__main__":
    verticals, horizontals = defaultdict(set), defaultdict(set)
    with open('input.txt', 'r') as input_file:
        for line in input_file:
            axe_a, axe_a_value, axe_b, axe_b_min, axe_b_max = PATTERN.match(line).groups()
            axe_a_value, axe_b_min, axe_b_max = int(axe_a_value), int(axe_b_min), int(axe_b_max)
            assert (axe_a != axe_b)
            if axe_b_min > axe_b_max:
                axe_b_min, axe_b_max = axe_b_max, axe_b_min
            if axe_a == 'x':
                verticals[axe_a_value].add((axe_b_min, axe_b_max))
            else:
                horizontals[axe_a_value].add((axe_b_min, axe_b_max))

    print(verticals)
    print(horizontals)

    print(solve(verticals, horizontals))

