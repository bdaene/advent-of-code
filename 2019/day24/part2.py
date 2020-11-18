
from collections import Counter

def solve(start_grid, nb_steps=200):
    grid = set()
    for r, row in enumerate(start_grid):
        for c, cell in enumerate(row):
            if cell == '#':
                grid.add((0, r, c))

    def show_grid():
        min_level = min(level for level, row, col in grid)
        max_level = max(level for level, row, col in grid)

        for level in range(min_level, max_level+1):
            s_grid = '\n'.join(''.join('#' if (level, row, col) in grid else '.' for col in range(5)) for row in range(5))
            print(f"Depth {level}:")
            print(s_grid)
            print()

    show_grid()

    for step in range(nb_steps):
        adjacent = Counter()
        for level, row, col in grid:
            # Top
            if row == 0:
                adjacent[(level - 1, 1, 2)] += 1
            elif row == 3 and col == 2:
                for c in range(5):
                    adjacent[(level + 1, 4, c)] += 1
            else:
                adjacent[(level, row - 1, col)] += 1
            # Bottom
            if row == 4:
                adjacent[(level - 1, 3, 2)] += 1
            elif row == 1 and col == 2:
                for c in range(5):
                    adjacent[(level + 1, 0, c)] += 1
            else:
                adjacent[(level, row + 1, col)] += 1
            # Left
            if col == 0:
                adjacent[(level - 1, 2, 1)] += 1
            elif row == 2 and col == 3:
                for r in range(5):
                    adjacent[(level + 1, r, 4)] += 1
            else:
                adjacent[(level, row, col - 1)] += 1
            # Right
            if col == 4:
                adjacent[(level - 1, 2, 3)] += 1
            elif row == 2 and col == 1:
                for r in range(5):
                    adjacent[(level + 1, r, 0)] += 1
            else:
                adjacent[(level, row, col + 1)] += 1

        grid &= adjacent.keys()

        for position, count in adjacent.items():
            if position in grid:
                if count != 1:
                    grid.remove(position)
            else:
                if 1 <= count <= 2:
                    grid.add(position)

    show_grid()

    return len(grid)


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        grid_ = list(line.strip() for line in input_file)
    print(solve(grid_))
