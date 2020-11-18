

from collections import deque


def solve(grid):
    print('\n'.join(grid))

    portals = {}
    known_portals = {}

    grid_ = [['.' for c in range(len(grid[r])-4)] for r in range(len(grid)-4)]

    for r, row in enumerate(grid[1:-1], -1):
        for c, cell in enumerate(row[1:-1], -1):
            if 'A' <= cell <= 'Z':
                name, position = '', (0, 0)
                if grid[2 + r + 1][2 + c] == '.':  # Above
                    name = grid[2 + r - 1][2 + c] + cell
                    position = (r + 1, c)
                elif grid[2 + r - 1][2 + c] == '.':  # Bottom
                    name = cell + grid[2 + r + 1][2 + c]
                    position = (r - 1, c)
                elif grid[2 + r][2 + c + 1] == '.':  # Left
                    name = grid[2 + r][2 + c - 1] + cell
                    position = (r, c + 1)
                elif grid[2 + r][2 + c - 1] == '.':  # Right
                    name = cell + grid[2 + r][2 + c + 1]
                    position = (r, c - 1)

                if name != '':
                    portal_r, portal_c = position
                    grid_[portal_r][portal_c] = '@'
                    if name in known_portals:
                        other_position = known_portals[name]
                        portals[position] = other_position
                        portals[other_position] = position
                        del known_portals[name]
                    else:
                        known_portals[name] = position

            elif cell in ' #' and 0 <= r < len(grid_) and 0 <= c < len(grid_[r]):
                grid_[r][c] = cell

    print(portals)
    print(known_portals)
    print('\n'.join(''.join(row) for row in grid_))

    start = known_portals['AA']
    end = known_portals['ZZ']

    queue = deque()
    queue.append((0, start))
    visited = {}
    while len(queue) > 0:
        steps, position = queue.popleft()
        if position == end:
            print('\n'.join(''.join(row) for row in grid_))
            return steps
        if position in visited:
            continue
        visited[position] = steps

        if position in portals:
            queue.append((steps + 1, portals[position]))

        r, c = position
        grid_[r][c] = f"{steps % 10}"
        if 0 < r and grid_[r-1][c] not in '# ':
            queue.append((steps + 1, (r - 1, c)))
        if 0 < c and grid_[r][c-1] not in '# ':
            queue.append((steps + 1, (r, c - 1)))
        if r < len(grid_)-1 and grid_[r + 1][c] not in '# ':
            queue.append((steps + 1, (r + 1, c)))
        if c < len(grid_[r])-1 and grid_[r][c + 1] not in '# ':
            queue.append((steps + 1, (r, c + 1)))


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        grid = list(line[:-1] for line in input_file)
    print(solve(grid))
