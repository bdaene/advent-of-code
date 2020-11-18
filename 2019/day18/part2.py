
from collections import deque
from heapq import heappush, heappop


def solve(grid):
    print('\n'.join(grid))
    print()

    keys = {}
    doors = {}
    starts = {}

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if 'a' <= cell <= 'z':
                assert(cell not in keys)
                keys[cell] = (r, c)
            elif 'A' <= cell <= 'Z':
                assert(cell not in doors)
                doors[cell] = (r, c)
            elif cell in '@&%*':
                starts[cell] = (r, c)
            elif cell in '.#':
                pass
            else:
                raise RuntimeError(f"Unknown cell {cell} at {(r, c)}")

    print(sorted(keys))
    print(sorted(doors))
    print(sorted(starts))
    print()

    def get_distances(start):
        distances = {}
        visited = set()
        queue = deque([(start, 0, frozenset())])
        while len(queue) > 0:
            position, distance, needed_keys = queue.popleft()
            if position in visited:
                continue
            visited.add(position)
            r, c = position
            cell = grid[r][c]
            if distance > 0 and cell in keys:
                distances[cell] = (distance, needed_keys)
            if cell in doors:
                needed_keys |= {cell.lower()}
            if cell != '#':
                distance += 1
                for r_, c_ in ((r + 1, c), (r-1, c), (r, c + 1), (r, c - 1)):
                    queue.append(((r_, c_), distance, needed_keys))

        return distances

    distances = {}
    for key in keys:
        distances[key] = get_distances(keys[key])
    for start in starts:
        distances[start] = get_distances(starts[start])

    print(distances)

    stack = [(0, len(keys), frozenset(starts), frozenset(keys), '')]
    seen = set()
    best = (len(keys), 0)
    while len(stack) > 0:
        steps, nb_missing_keys, positions, missing_keys, path = heappop(stack)
        if (positions, missing_keys) in seen:
            continue
        seen.add((positions, missing_keys))
        if (nb_missing_keys, steps) <= best:
            print(len(stack), steps, nb_missing_keys, positions, missing_keys, path)
            best = (nb_missing_keys, steps)
        if nb_missing_keys == 0:
            return steps, path
        for position in positions:
            for next_key, (dist, needed_keys) in distances[position].items():
                if next_key in missing_keys and needed_keys.isdisjoint(missing_keys):
                    next_positions = positions - {position} | {next_key}
                    heappush(stack, (steps + dist, nb_missing_keys - 1, next_positions, missing_keys - {next_key}, path + next_key))


if __name__ == "__main__":
    with open('input2.txt', 'r') as input_file:
        grid = list(line.strip() for line in input_file)
    print(solve(grid))
