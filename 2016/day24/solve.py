from heapq import heappush, heappop
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


@timeit
def part_1(data):
    pos = None
    all_keys = set()
    for row, line in enumerate(data):
        for col, key in enumerate(line):
            if key == '0':
                pos = (row, col)
            if '0' <= key <= '9':
                all_keys.add(key)

    # state = (nb_steps, -nb_keys, keys, pos)
    keys = frozenset('0')
    heap = [(0, 0, keys, pos)]
    seen = {(keys, pos)}
    while heap:
        nb_steps, _, keys, pos = heappop(heap)
        if keys == all_keys:
            return nb_steps

        row, col = pos
        for r, c in ((row-1, col), (row+1, col), (row, col-1), (row, col+1)):
            if 0 <= r <= len(data) and 0 <= c <= len(data[r]) and data[r][c] != '#':
                key = data[r][c]
                keys_ = (keys | {key}) if key in all_keys else keys
                pos_ = (r, c)
                if (keys_, pos_) not in seen:
                    seen.add((keys_, pos_))
                    heappush(heap, (nb_steps + 1, -len(keys_), keys_, pos_))


@timeit
def part_2(data):
    start_pos = None
    all_keys = set()
    for row, line in enumerate(data):
        for col, key in enumerate(line):
            if key == '0':
                start_pos = (row, col)
            if '0' <= key <= '9':
                all_keys.add(key)

    # state = (nb_steps, -nb_keys, dist(pos, start_pos)), keys, pos)
    keys = frozenset('0')
    heap = [(0, 0, 0, keys, start_pos)]
    seen = {(keys, start_pos)}
    while heap:
        nb_steps, _, _, keys, pos = heappop(heap)
        if keys == all_keys and pos == start_pos:
            return nb_steps

        row, col = pos
        for r, c in ((row-1, col), (row+1, col), (row, col-1), (row, col+1)):
            if 0 <= r <= len(data) and 0 <= c <= len(data[r]) and data[r][c] != '#':
                key = data[r][c]
                keys_ = (keys | {key}) if key in all_keys else keys
                pos_ = (r, c)
                if (keys_, pos_) not in seen:
                    seen.add((keys_, pos_))
                    dist = abs(pos_[0] - start_pos[0]) + abs(pos_[1] - start_pos[1])
                    heappush(heap, (nb_steps + 1, -len(keys_), dist, keys_, pos_))
    return len(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
