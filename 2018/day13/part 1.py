

def solve(input_file):
    grid = list(list(line[:-1]) for line in input_file)
    carts = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '^':
                carts.append((row, col, '^', '|', 'left'))
            elif grid[row][col] == 'v':
                carts.append((row, col, 'v', '|', 'left'))
            elif grid[row][col] == '>':
                carts.append((row, col, '>', '-', 'left'))
            elif grid[row][col] == '<':
                carts.append((row, col, '<', '-', 'left'))


    def advance_time():
        carts.sort()
        collisions = []
        for cart, (row, col, dir, track, action) in enumerate(carts):
            if dir == 'X':
                continue
            grid[row][col] = track
            if dir == '^':
                row -= 1
                if grid[row][col] == '\\':
                    dir = '<'
                elif grid[row][col] == '/':
                    dir = '>'
            elif dir == 'v':
                row += 1
                if grid[row][col] == '\\':
                    dir = '>'
                elif grid[row][col] == '/':
                    dir = '<'
            elif dir == '>':
                col += 1
                if grid[row][col] == '\\':
                    dir = 'v'
                elif grid[row][col] == '/':
                    dir = '^'
            elif dir == '<':
                col -= 1
                if grid[row][col] == '\\':
                    dir = '^'
                elif grid[row][col] == '/':
                    dir = 'v'

            if grid[row][col] in '^v><':
                collisions.append((row, col))
                other_cart = 0
                while carts[other_cart][:2] != (row, col):
                    other_cart += 1
                carts[other_cart] = carts[other_cart][:2] + ('X',) + carts[other_cart][3:]
                grid[row][col] = carts[other_cart][3]
                dir = 'X'

            elif grid[row][col] == '+':
                if action == 'left':
                    action = 'straight'
                    dir = {'^': '<', '<': 'v', 'v': '>', '>': '^'}[dir]
                elif action == 'straight':
                    action = 'right'
                elif action == 'right':
                    action = 'left'
                    dir = {'^': '>', '>': 'v', 'v': '<', '<': '^'}[dir]

            track = grid[row][col]
            if dir != 'X':
                grid[row][col] = dir
            carts[cart] = (row, col, dir, track, action)
        return collisions

    def show_grid():
        print(carts)
        print('\n'.join(''.join(line) for line in grid))

    # show_grid()
    total_collisions = 0
    while total_collisions*2 + 1 < len(carts):
        # input()
        collisions = advance_time()
        # show_grid()
        if collisions:
            total_collisions += len(collisions)
            print(collisions)

    print(carts)
    return list(cart[:2] for cart in carts if cart[2] != 'X')


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
