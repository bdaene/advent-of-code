from heapq import heappush, heappop
from utils import timeit


def is_open(coordinate, offset=1362):
    x, y = coordinate
    if x < 0 or y < 0:
        return False
    v = x*x + 3*x + 2*x*y + y + y*y + offset
    c = 0
    while v > 0:
        c += 1
        v &= v - 1
    return c & 1 == 0


@timeit
def part_1(start=(1, 1), target=(31, 39)):
    heap = [(0, start)]
    seen = {start}
    while heap:
        dist, (x, y) = heappop(heap)
        if (x, y) == target:
            return dist

        for x_, y_ in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            pos = (x_, y_)
            if is_open(pos) and pos not in seen:
                seen.add(pos)
                heappush(heap, (dist+1, pos))


@timeit
def part_2(start=(1, 1), max_dist=50):
    heap = [(0, start)]
    seen = {start}
    while heap:
        dist, (x, y) = heappop(heap)
        if dist >= max_dist:
            return len(seen)

        for x_, y_ in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            pos = (x_, y_)
            if is_open(pos) and pos not in seen:
                seen.add(pos)
                heappush(heap, (dist + 1, pos))


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
