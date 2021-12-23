from functools import cache
from heapq import heappop, heappush

from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return tuple(line[:-1] for line in input_file)


MOVE_COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


def get_all_allowed_moves(positions, paths, max_depth):
    occupied_positions = {(room, depth): a for a, room, depth in positions}
    moves = set()
    for position in positions:
        a, room, index = position
        move_cost = MOVE_COST[a]
        if room == 'H':
            for end, cost, path in paths[(room, index)]:
                if a == end[0] and all(occupied_positions.get((a, i)) == a for i in range(end[1] + 1, max_depth)):
                    if not (occupied_positions.keys() & path):
                        moves.add((position, (a,) + end, cost * move_cost))
        else:
            for end, cost, path in paths[(room, index)]:
                if a != room or any(occupied_positions.get((a, i)) != a for i in range(end[1] + 1, max_depth)):
                    if not (occupied_positions.keys() & path):
                        moves.add((position, (a,) + end, cost * move_cost))
    return frozenset(moves)


def get_paths(max_depth):
    paths = {}
    # From room 0 to hall
    for i, position in zip((-3, -1, 1, 3), ((r, 0) for r in 'ABCD')):
        paths[position] = []
        # Going left
        cost, path = 0, set()
        for end in range(i - 1, -5, -2):
            cost += 2
            path.add(('H', end))
            paths[position].append((('H', end), cost, frozenset(path)))
        cost += 1
        path.add(('H', -5))
        paths[position].append((('H', -5), cost, frozenset(path)))
        # Going right
        cost, path = 0, set()
        for end in range(i + 1, 5, 2):
            cost += 2
            path.add(('H', end))
            paths[position].append((('H', end), cost, frozenset(path)))
        cost += 1
        path.add(('H', 5))
        paths[position].append((('H', 5), cost, frozenset(path)))

        paths[position] = frozenset(paths[position])

    # From deeper rooms to hall
    for room in 'ABCD':
        for depth in range(1, max_depth):
            paths[(room, depth)] = frozenset((end, cost + 1, path | {(room, depth - 1)})
                                             for end, cost, path in paths[(room, depth - 1)])

    # From hall to rooms:
    hall_paths = {h: set() for h in (('H', i) for i in (-5, -4, -2, 0, 2, 4, 5))}
    for room in paths:
        for end, cost, path in paths[room]:
            hall_paths[end].add((room, cost, path - {end} | {room}))
    for h, p in hall_paths.items():
        paths[h] = frozenset(p)

    return paths


ROOM_ENTRIES = {r: i for r, i in zip('ABCD', (-3, -1, 1, 3))}


@cache
def estimate_cost(positions):
    cost = 0
    for a, room, index in positions:
        if a == room:
            continue
        if room == 'H':
            cost += (1 + abs(index - ROOM_ENTRIES[a])) * MOVE_COST[a]
        else:
            cost += (2 + index + abs(ROOM_ENTRIES[room] - ROOM_ENTRIES[a])) * MOVE_COST[a]
    return cost


@timeit
def part_1(data):
    rooms = {r: [line[3 + i * 2] for line in data[2:-1]] for i, r in enumerate('ABCD')}
    positions = frozenset((a, r, i) for r, room in rooms.items() for i, a in enumerate(room))
    max_depth = len(data) - 3
    target = frozenset((r, r, d) for r in 'ABCD' for d in range(max_depth))
    paths = get_paths(max_depth)

    heap = [(estimate_cost(positions), 0, positions)]
    seen_positions = {positions}
    while heap:
        estimated_total_cost, total_cost, positions = heappop(heap)
        if positions == target:
            return total_cost
        for start, end, cost in get_all_allowed_moves(positions, paths, max_depth):
            new_positions = positions - {start} | {end}
            if new_positions in seen_positions:
                continue
            seen_positions.add(new_positions)
            new_total_cost = total_cost + cost
            new_estimated_total_cost = new_total_cost + estimate_cost(new_positions)
            heappush(heap, (new_estimated_total_cost,  new_total_cost, new_positions))


@timeit
def part_2(data):
    data = data[:3] + ('  #D#C#B#A#  ', '  #D#B#A#C#  ') + data[3:]
    return part_1.func(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
