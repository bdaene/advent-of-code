

def solve(grid):
    start = 0
    next_weight, weights = 1, []
    for row in grid:
        for cell in row:
            weights.append(next_weight)
            if cell == '#':
                start += next_weight
            next_weight <<= 1

    width, height = len(grid[0]), len(grid)
    adjacent = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            adj = 0
            if r > 0:
                adj += weights[(r - 1) * width + c]
            if c > 0:
                adj += weights[r * width + c - 1]
            if r < height - 1:
                adj += weights[(r + 1) * width + c]
            if c < width - 1:
                adj += weights[r * width + c + 1]
            adjacent.append(adj)

    seen = set()
    configuration = start
    while configuration not in seen:
        seen.add(configuration)
        configuration_ = 0
        for i, weight in enumerate(weights):
            adj = configuration & adjacent[i]
            count = 0
            while adj > 0:
                count += 1
                adj &= adj - 1

            if configuration & weight :
                if count == 1:
                    configuration_ += weight
            else:
                if 1 <= count <= 2:
                    configuration_ += weight

        configuration = configuration_

    return configuration


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        grid_ = list(line.strip() for line in input_file)
    print(solve(grid_))
