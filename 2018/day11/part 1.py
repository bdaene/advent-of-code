
import re

PATTERN = re.compile(r'position=<\s*(-?\d*),\s*(-?\d*)> velocity=<\s*(-?\d*),\s*(-?\d*)>')


def solve(grid_serial=1308, grid_size=300):

    def cell_value(x, y):
        rack_id = x + 10
        cell_power = rack_id * y
        cell_power += grid_serial
        cell_power *= rack_id
        cell_power = (cell_power % 1000) // 100
        cell_power -= 5
        return cell_power

    grid = [[cell_value(x + 1, y + 1) for x in range(grid_size)] for y in range(grid_size)]
    sum_grid = [[0] * grid_size for _ in range(grid_size)]
    for x in range(grid_size):
        for y in range(grid_size):
            a = sum_grid[x - 1][y - 1] if x > 0 and y > 0 else 0
            b = sum_grid[x - 1][y] if x > 0 else 0
            c = sum_grid[x][y - 1] if y > 0 else 0
            sum_grid[x][y] = b + c - a + grid[x][y]

    def get_best_square(square_size=3):
        best_square = -1000000, 0, 0
        for x in range(grid_size-square_size+1):
            for y in range(grid_size-square_size+1):
                a = sum_grid[x - 1][y - 1] if x > 0 and y > 0 else 0
                b = sum_grid[x + square_size - 1][y - 1] if y > 0 else 0
                c = sum_grid[x - 1][y + square_size - 1] if x > 0 else 0
                d = sum_grid[x + square_size - 1][y + square_size - 1]
                square_power = d - b - c + a
                if square_power > best_square[0]:
                    best_square = square_power, x, y

        return best_square

    best = 0, 0, 0, 0
    for square_size in range(1, grid_size + 1):
        power, x, y = get_best_square(square_size)
        if power > best[0]:
            best = power, y+1, x+1, square_size
            print(best)
    return best


if __name__ == "__main__":
    print(solve())
