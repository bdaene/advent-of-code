import hashlib
from heapq import heappush, heappop
from utils import timeit


def gen_next_rooms(data, x, y, path):
    key = hashlib.md5(data + path).hexdigest()
    if y > 0 and 'b' <= key[0] <= 'f':
        yield x, y - 1, path + b'U'
    if y < 3 and 'b' <= key[1] <= 'f':
        yield x, y + 1, path + b'D'
    if x > 0 and 'b' <= key[2] <= 'f':
        yield x - 1, y, path + b'L'
    if x < 3 and 'b' <= key[3] <= 'f':
        yield x + 1, y, path + b'R'


@timeit
def part_1(data):
    heap = [(0, (0, 0, b''))]
    while heap:
        dist, room = heappop(heap)
        if room[:2] == (3, 3):
            return room[2]
        for room_ in gen_next_rooms(data, *room):
            heappush(heap, (dist + 1, room_))


@timeit
def part_2(data):
    best = (0, (0, 0, b''))
    heap = [(0, (0, 0, b''))]
    while heap:
        dist, room = heappop(heap)
        if room[:2] == (3, 3):
            print(dist, room)
            best = (dist, room)
        else:
            for room_ in gen_next_rooms(data, *room):
                heappush(heap, (dist + 1, room_))
    return best[0]


def main():
    data = b'rrrbmfta'
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
