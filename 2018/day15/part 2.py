
from collections import deque

DEBUG = False


def solve(grid, elves_attack=3):

    grid = list(list(cell for cell in row) for row in grid)

    class Unit:
        def __init__(self, row, col, unit_class):
            self.row = row
            self.col = col
            self.unit_class = unit_class
            self.hit_points = 200
            self.attack_power = 3 if unit_class == 'G' else elves_attack

        def __str__(self):
            return f"{self.unit_class}({self.hit_points})"

    units = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in 'GE':
                units.append(Unit(r, c, cell))

    def show():
        for r, row in enumerate(grid):
            s = ''.join(row) + '   '
            units_in_row = [unit for unit in units if unit.row == r and unit.hit_points > 0]
            units_in_row.sort(key=lambda unit_ : unit_.col)
            s += ', '.join(str(unit) for unit in units_in_row)
            print(s)
        print()

    print('Initially:')
    show()

    def combat():
        nb_round = 0
        while True:
            # Round
            units.sort(key=lambda unit_: (unit_.row, unit_.col))
            for unit in units:
                # Turn
                if unit.hit_points <= 0:
                    continue
                if DEBUG:
                    print(f"Turn of unit {unit} at position ({unit.row}, {unit.col})")

                targets = list(target for target in units if unit.unit_class != target.unit_class and target.hit_points > 0)
                if len(targets) == 0:
                    return nb_round

                in_range = []
                for target in targets:
                    in_range.extend((r, c) for r, c in ((target.row - 1, target.col),
                                                        (target.row + 1, target.col),
                                                        (target.row, target.col - 1),
                                                        (target.row, target.col + 1))
                                    if grid[r][c] == '.' or (r, c) == (unit.row, unit.col))
                if DEBUG:
                    print(in_range)

                is_in_range = (unit.row, unit.col) in in_range
                if DEBUG:
                    print(is_in_range)

                if not is_in_range:
                    if len(in_range) == 0:
                        continue
                    else:
                        # Move
                        distances = {}
                        queue = deque()
                        queue.append((unit.row, unit.col, 0))
                        while len(queue) > 0:
                            row, col, steps = queue.popleft()
                            if (row, col) in distances:
                                continue
                            distances[(row, col)] = steps
                            for r, c in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
                                if grid[r][c] == '.':
                                    queue.append((r, c, steps + 1))

                        in_range_squares = {square: distances[square] for square in in_range if square in distances}
                        if DEBUG:
                            print(in_range_squares)

                        if len(in_range_squares) == 0:
                            continue
                        min_steps = min(in_range_squares.values())
                        chosen = sorted(square for square, distance in in_range_squares.items() if distance == min_steps)[0]
                        if DEBUG:
                            print(chosen)

                        paths = {chosen}
                        distance = distances[chosen]
                        while distance > 1:
                            distance -= 1
                            paths_ = set()
                            for row, col in paths:
                                for r, c in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
                                    if (r, c) in distances and distances[(r, c)] == distance:
                                        paths_.add((r, c))
                            paths = paths_
                        if DEBUG:
                            print(paths)

                        step = sorted(paths)[0]
                        grid[unit.row][unit.col] = '.'
                        unit.row, unit.col = step
                        grid[unit.row][unit.col] = unit.unit_class

                # Attack
                in_range = [target for target in targets
                            if abs(target.row - unit.row) + abs(target.col - unit.col) == 1]
                if len(in_range) == 0:
                    continue
                target = sorted(in_range, key=lambda target_: (target_.hit_points, target_.row, target_.col))[0]

                target.hit_points -= unit.attack_power
                if target.hit_points <= 0:
                    if target.unit_class == 'E':
                        return -1
                    grid[target.row][target.col] = '.'

            nb_round += 1
            # print(f"After {nb_round} round:")
            # show()

    nb_rounds = combat()
    if nb_rounds < 0:
        return nb_rounds

    print(f"Combat finished after {nb_rounds} round:")
    show()
    return nb_rounds * sum(unit.hit_points for unit in units if unit.hit_points > 0)


if __name__ == "__main__":
    with open("input.txt", 'r') as input_file:
        grid = tuple(tuple(line.strip()) for line in input_file)
    min_attack = 3
    max_attack = 3
    while solve(grid, elves_attack=max_attack) < 0:
        max_attack *= 2
    while min_attack + 1 < max_attack:
        mid_attack = (min_attack + max_attack) // 2
        if solve(grid, elves_attack=mid_attack) < 0:
            min_attack = mid_attack
        else:
            max_attack = mid_attack

    print(f"Attack set to {max_attack}")
    print(f"Attack set to {max_attack}. Outcome: {solve(grid, elves_attack=max_attack)}")
