from collections import defaultdict
from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return input_file.readline().strip()


def create_map(regex):
    grid = defaultdict(lambda: '?')

    positions = [{0}]
    ends = []
    directions = {'N': 1j, 'S': -1j, 'E': 1, 'W': -1}

    for c in regex[1:-1]:
        if c == '(':
            positions.append(set(positions[-1]))
            ends.append(set())
        elif c == '|':
            ends[-1] |= positions[-1]
            positions[-1] = set(positions[-2])
        elif c == ')':
            ends[-1] |= positions.pop()
            positions[-1] = ends.pop()
        elif c in directions:
            new_positions = set()
            direction = directions[c]
            for position in positions[-1]:
                grid[position + direction] = ' '
                grid[position + 2 * direction] = ' '
                new_positions.add(position + 2 * direction)
            positions[-1] = new_positions
        else:
            raise ValueError(f"Unknown instruction {c}.")

    grid[0] = 'X'

    # show_map(grid)

    return grid


def show_map(grid):
    row_min = int(-max(pos.imag for pos in grid)) - 1
    row_max = int(-min(pos.imag for pos in grid)) + 1
    col_min = int(min(pos.real for pos in grid)) - 1
    col_max = int(max(pos.real for pos in grid)) + 1

    print('\n'.join(''.join(grid[col - 1j * row]
                            for col in range(col_min, col_max+1))
                    for row in range(row_min, row_max+1)))


def get_distances(grid):
    distances = {}
    stack = [(0, 0)]
    while stack:
        pos, dist = stack.pop()
        if pos in distances and dist >= distances[pos]:
            continue
        distances[pos] = dist
        for direction in (-1, +1, -1j, +1j):
            if grid[pos + direction] == ' ':
                stack.append((pos + 2*direction, dist + 1))
    return distances


@timeit
def part_1(data):
    grid = create_map(data)
    distances = get_distances(grid)
    return max(distances.values())


@timeit
def part_2(data):
    grid = create_map(data)
    distances = get_distances(grid)
    return sum(1 for pos, dist in distances.items() if dist >= 1000)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
