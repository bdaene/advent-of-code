from collections import defaultdict
from utils import timeit


@timeit
def part_1(data):
    n = 1
    while n**2 < data:
        n += 2
    data -= (n-2)**2
    data %= n

    n2 = (n-1)//2
    return abs(data - (n2-1)) + n2


def show_grid(grid):
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)
    for y in range(max_y, min_y-1, -1):
        for x in range(min_x, max_x+1):
            print(f"{grid[(x,y)]:8}", end='')
        print()


@timeit
def part_2(data):

    grid = defaultdict(int)
    grid[(0, 0)] = 1
    x, y = 0, 0
    dx, dy = 1, 0
    while True:
        x += dx
        y += dy
        grid[(x, y)] = sum(grid[(x+a, y+b)] for a in range(-1, 2) for b in range(-1, 2))
        if grid[(x, y)] > data:
            show_grid(grid)
            return grid[(x, y)]

        if grid[(x-dy, y+dx)] == 0:
            dx, dy = -dy, dx


def main():
    data = 347991
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
