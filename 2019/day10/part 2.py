
def gcd(a,b):
    while a:
        a, b = b % a, a
    return b


def solve(input_file):

    asteroids = set()
    for y, line in enumerate(input_file):
        for x, cell in enumerate(line.strip()):
            if cell == '#':
                asteroids.add((x,y))

    best = None
    for asteroid in asteroids:
        x, y = asteroid
        lines = set()
        for asteroid_ in asteroids:
            if asteroid == asteroid_:
                continue
            dx, dy = asteroid_[0]-asteroid[0], asteroid_[1]-asteroid[1]
            g = gcd(abs(dx), abs(dy))
            lines.add((dx//g, dy//g))

        if best is None or len(lines) > best[0]:
            best = len(lines), asteroid

    station = best[1]
    asteroids.remove(station)
    print(f"Station placed at {station}, visible : {best[0]}")

    target = None
    for asteroid in asteroids:
        if asteroid[0] == station[0] and asteroid[1] < station[1]:
            if target is None or target[1] < asteroid[1]:
                target = asteroid

    count = 0
    if target is not None:
        asteroids.remove(target)
        count += 1
        print(f"The {count} asteroid to be vaporized is at {target}")
    else:
        target = (station[0],station[1])

    while count < 200:
        next_target = None
        for asteroid in asteroids:
            if (asteroid[0] - station[0])*(target[1] - station[1]) - (asteroid[1] - station[1])*(target[0] - station[0]) < 0:
                if next_target is None:
                    next_target = asteroid
                else:
                    test2 = (next_target[0] - station[0])*(asteroid[1] - station[1]) - (next_target[1] - station[1])*(asteroid[0] - station[0])
                    if test2 < 0 or (test2 == 0 and abs(next_target[0]-station[0])+abs(next_target[1]-station[1]) > abs(asteroid[0]-station[0])+abs(asteroid[1]-station[1])):
                        next_target = asteroid

        if next_target is None:
            target = (2 * station[0] - target[0], 2 * station[1] - target[1])
            for asteroid in asteroids:
                if (asteroid[0] - station[0]) * (target[1] - station[1]) - (asteroid[1] - station[1]) * (
                    target[0] - station[0]) == 0:
                    if next_target is None:
                        next_target = asteroid
                    else:
                        test2 = (next_target[0] - station[0]) * (asteroid[1] - station[1]) - (
                                    next_target[1] - station[1]) * (asteroid[0] - station[0])
                        if test2 < 0 or (
                                test2 == 0 and abs(next_target[0] - station[0]) + abs(next_target[1] - station[1]) > abs(
                                asteroid[0] - station[0]) + abs(asteroid[1] - station[1])):
                            next_target = asteroid

        if next_target is None:
            target = (2 * station[0] - target[0], 2 * station[1] - target[1])
            for asteroid in asteroids:
                if (asteroid[0] - station[0]) * (target[1] - station[1]) - (asteroid[1] - station[1]) * (
                    target[0] - station[0]) == 0:
                    if next_target is None:
                        next_target = asteroid
                    elif abs(next_target[0] - station[0]) + abs(next_target[1] - station[1]) > abs(asteroid[0] - station[0]) + abs(asteroid[1] - station[1]):
                        next_target = asteroid

        asteroids.remove(next_target)
        count += 1
        print(f"The {count} asteroid to be vaporized is at {next_target}")
        target = next_target

    return target


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))