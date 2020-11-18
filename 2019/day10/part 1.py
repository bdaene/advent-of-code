
def gcd(a,b):
    while a:
        a, b = b % a, a
    return b


def solve(input_file):

    asteroids = []
    for y, line in enumerate(input_file):
        for x, cell in enumerate(line.strip()):
            if cell == '#':
                asteroids.append((x,y))

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

    return best


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))