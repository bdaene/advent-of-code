from collections import deque

from utils import timeit


@timeit
def get_data():
    grid, start, end = {}, None, None
    with open('input.txt') as input_file:
        for row, line in enumerate(input_file):
            for col, cell in enumerate(line.strip()):
                if cell == 'S':
                    start = (row, col)
                    cell = 'a'
                elif cell == 'E':
                    end = (row, col)
                    cell = 'z'
                grid[(row, col)] = ord(cell) - ord('a')
    return grid, start, end


def get_neighbors(a: tuple[int, int], grid: dict[tuple[int, int], int]):
    x, y = a
    h = grid[a]
    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if (nx, ny) in grid and grid[(nx, ny)] >= h - 1:
            yield nx, ny


def get_distances(grid, position):
    queue = deque([position])
    distances = {position: 0}

    while queue:
        position = queue.popleft()
        for neighbor in get_neighbors(position, grid):
            if neighbor in distances:
                continue
            distances[neighbor] = distances[position] + 1
            queue.append(neighbor)

    return distances


@timeit
def part_1(grid, start, end):
    distances = get_distances(grid, end)
    return distances[start]


@timeit
def part_2(grid, _, end):
    distances = get_distances(grid, end)
    return min(distances[position] for position in distances if grid[position] == 0)


def main():
    data = get_data()
    part_1(*data)
    part_2(*data)


if __name__ == "__main__":
    main()
