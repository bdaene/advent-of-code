
import re

PATTERN = re.compile(r'position=<\s*(-?\d*),\s*(-?\d*)> velocity=<\s*(-?\d*),\s*(-?\d*)>')


def solve(input_file):
    stars = []
    for line in input_file:
        x, y, vx, vy = map(int, PATTERN.match(line).groups())
        stars.append((x, y, vx, vy))

    time, time_direction = 0, 1
    previous_dx, previous_dy = 1000000, 1000000
    while True:
        spots = set()
        x, y, vx, vy = stars[0]
        spots.add((x, y))
        min_x = max_x = x + time * vx
        min_y = max_y = y + time * vy
        for x, y, vx, vy in stars[1:]:
            x += vx * time
            y += vy * time
            spots.add((x,y))
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        if time_direction < 0 or max_y - min_x > previous_dx or max_y - min_y > previous_dy:
            print(time, min_x, max_x, min_y, max_y)
            print('\n'.join(''.join('#' if (x, y) in spots else '.' for x in range(min_x, max_x + 1)) for y in
                            range(min_y, max_y + 1)))
            input()
            time_direction = -1

        previous_dx, previous_dy = max_x-min_x, max_y-min_y
        time += time_direction


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        solve(input_file)
