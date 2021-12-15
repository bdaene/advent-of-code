import numpy
from utils import timeit
from heapq import heappush, heappop


@timeit
def get_data():
    with open('input.txt') as input_file:
        return numpy.array([list(map(int, line.strip())) for line in input_file])


@timeit
def part_1(data):
    h, w = data.shape
    h -= 1
    w -= 1

    heap = [(0, 0, 0)]
    seen = {(0, 0)}
    while heap:
        cost, x, y = heappop(heap)

        if (x, y) == (h, w):
            return cost

        for x_, y_ in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if 0 <= x_ <= w and 0 <= y_ <= h and (x_, y_) not in seen:
                seen.add((x_, y_))
                heappush(heap, (cost + data[x_, y_], x_, y_))


@timeit
def part_2(data):
    h, w = data.shape
    grid = numpy.full((h*5, w*5), 0)
    for x in range(5):
        for y in range(5):
            grid[x*w:(x+1)*w, y*w:(y+1)*w] = (data - 1 + x + y) % 9 + 1

    return part_1.func(grid)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
