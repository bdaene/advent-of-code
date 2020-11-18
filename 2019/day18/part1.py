
from collections import deque
from heapq import heappush, heappop


def solve(grid):
    print('\n'.join(grid))
    print()

    keys = {}
    doors = {}
    start = (0, 0)

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if 'a' <= cell <= 'z':
                assert(cell not in keys)
                keys[cell] = (r, c)
            elif 'A' <= cell <= 'Z':
                assert(cell not in doors)
                doors[cell] = (r, c)
            elif cell in '@&%*':
                start = (r, c)
            elif cell in '.#':
                pass
            else:
                raise RuntimeError(f"Unknown cell {cell} at {(r, c)}")

    print(sorted(keys))
    print(sorted(doors))
    print(start)
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

    distances = {'@': get_distances(start)}
    for key in keys:
        distances[key] = get_distances(keys[key])

    print(distances)

    stack = [(0, len(keys), '@', frozenset(keys), '')]
    seen = set()
    best = (len(keys), 0)
    while len(stack) > 0:
        steps, nb_missing_keys, position, missing_keys, path = heappop(stack)
        if (position, missing_keys) in seen:
            continue
        seen.add((position, missing_keys))
        if (nb_missing_keys, steps) <= best:
            print(len(stack), steps, nb_missing_keys, position, missing_keys, path)
            best = (nb_missing_keys, steps)
        if nb_missing_keys == 0:
            return steps, path
        for next_key, (dist, needed_keys) in distances[position].items():
            if next_key in missing_keys and needed_keys.isdisjoint(missing_keys):
                heappush(stack, (steps + dist, nb_missing_keys - 1, next_key, missing_keys - {next_key}, path + next_key))


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        grid = list(line.strip() for line in input_file)
    print(solve(grid))
