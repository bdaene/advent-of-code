

from collections import deque


def solve(grid):
    print('\n'.join(''.join(row) for row in grid))

    portals = {}
    known_portals = {}
    portals_name = {}

    for r, row in enumerate(grid[1:-1], 1):
        for c, cell in enumerate(row[1:-1], 1):
            if 'A' <= cell <= 'Z':
                name, position = '', (0, 0)
                if grid[r + 1][c] == '.':  # Above
                    name = grid[r - 1][c] + cell
                    position = (r + 1, c)
                elif grid[r - 1][c] == '.':  # Bottom
                    name = cell + grid[r + 1][c]
                    position = (r - 1, c)
                elif grid[r][c + 1] == '.':  # Left
                    name = grid[r][c - 1] + cell
                    position = (r, c + 1)
                elif grid[r][c - 1] == '.':  # Right
                    name = cell + grid[r][c + 1]
                    position = (r, c - 1)

                if name != '':
                    portals_name[position] = name
                    portal_r, portal_c = position
                    inside = 2 < portal_r < len(grid) - 3 and 2 < portal_c < len(grid[portal_r]) - 3
                    grid[portal_r][portal_c] = '@' if inside else '$'
                    if name in known_portals:
                        other_position = known_portals[name]
                        portals[position] = other_position
                        portals[other_position] = position
                        del known_portals[name]
                    else:
                        known_portals[name] = position

    print(portals)
    print(known_portals)
    print('\n'.join(''.join(row) for row in grid))

    start = (0, known_portals['AA'])
    end = (0, known_portals['ZZ'])

    queue = deque()
    queue.append((0, start, 'AA'))
    visited = {}
    max_level, max_queue = 0, 0
    while len(queue) > 0:
        steps, position, path = queue.popleft()
        if position in visited:
            continue
        visited[position] = steps

        level, (r, c) = position
        max_level = max(max_level, level)
        max_queue = max(max_queue, len(queue))
        if position == end:
            print(path + f"{grid[r][c]}{portals_name[(r, c)]}")
            print(f"Max level: {max_level}")
            print(f"Max queue length: {max_queue}")
            return steps

        if (r, c) in portals:
            next_level = level + (1 if grid[r][c] == '@' else -1)
            if next_level >= 0:
                queue.append((steps + 1,
                              (next_level, portals[(r, c)]),
                              path + f"{grid[r][c]}{portals_name[(r, c)]}"))

        if 0 < r and grid[r-1][c] in '.@$':
            queue.append((steps + 1, (level, (r - 1, c)), path))
        if 0 < c and grid[r][c-1] in '.@$':
            queue.append((steps + 1, (level, (r, c - 1)), path))
        if r < len(grid)-1 and grid[r + 1][c] in '.@$':
            queue.append((steps + 1, (level, (r + 1, c)), path))
        if c < len(grid[r])-1 and grid[r][c + 1] in '.@$':
            queue.append((steps + 1, (level, (r, c + 1)), path))


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        grid = list(list(line[:-1]) for line in input_file)
    print(solve(grid))
