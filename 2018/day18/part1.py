

from collections import Counter


def parse():
    grid = []
    with open('input.txt', 'r') as input_file:
        for line_ in input_file:
            grid.append(list(line_[:-1]))

    return grid


def solve(grid, max_time = 1000000000):

    def show_grid():
        # print('\n1'.join(''.join(line) for line in grid))
        count = Counter(cell for r, row in enumerate(grid) for c, cell in enumerate(row))
        # print(f"Open {count['.']}, trees {count['|']}, lumberyard {count['#']}")
        # print(f"Total resource value {count['|'] * count['#']}")
        print(f"{count['|'] * count['#']}")
        # print()

    grid_s = '\n'.join(''.join(line) for line in grid)
    seen_grid = {}

    print(grid_s)

    for t in range(max_time + 1):
        grid_s = '\n'.join(''.join(line) for line in grid)
        print(f"Time = {t}")
        print(grid_s)

        if t == max_time or (grid_s in seen_grid and (max_time - seen_grid[grid_s]) % (t-seen_grid[grid_s]) == 0):
            count = Counter(cell for r, row in enumerate(grid) for c, cell in enumerate(row))
            print(f"Open {count['.']}, trees {count['|']}, lumberyard {count['#']}")
            print(f"Total resource value {count['|'] * count['#']}")
            return count['|'] * count['#']
        else:
            seen_grid[grid_s] = t

        modified = {}
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                count = Counter(grid[r_][c_]
                                for r_ in range(r-1, r+2)
                                for c_ in range(c-1, c+2)
                                if 0 <= r_ < len(grid) and 0 <= c_ < len(grid[r_]) and (r_, c_) != (r, c))
                if cell == '.':
                    if count['|'] >= 3:
                        modified[(r, c)] = '|'
                elif cell == '|':
                    if count['#'] >= 3:
                        modified[(r, c)] = '#'
                elif cell == '#':
                    if count['#'] >= 1 and count['|'] >= 1:
                        pass
                    else:
                        modified[(r, c)] = '.'
                else:
                    raise RuntimeError(f"Unknown content {cell} in row {r}, col {c}.")

        for (r, c), value in modified.items():
            grid[r][c] = value

        show_grid()


if __name__ == "__main__":
    print(solve(parse()))
