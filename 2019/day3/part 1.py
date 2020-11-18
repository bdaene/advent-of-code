
def solve(input_file):
    path1 = get_path(input_file.readline().split(','))
    path2 = get_path(input_file.readline().split(','))

    # path1 = get_path("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(","))
    # path2 = get_path("U62,R66,U55,R34,D71,R55,D58,R83".split(","))
    print(path1)
    print(path2)

    best = None
    p1 = path1[0]
    for p2 in path1[1:]:
        p3 = path2[0]
        for p4 in path2[1:]:
            intersection = get_intersection(p1, p2, p3, p4)
            if intersection is not None and intersection != (0, 0):
                print(intersection)
                if best is None or sum(map(abs, intersection)) < sum(map(abs, best)):
                    best = intersection
            p3 = p4
        p1 = p2
    return best


def get_path(directions):
    x, y = 0, 0
    path = []
    for direction in directions:
        path.append((x, y))
        distance = int(direction[1:])
        if direction[0] == "U":
            y += distance
        elif direction[0] == "D":
            y -= distance
        elif direction[0] == "R":
            x += distance
        elif direction[0] == "L":
            x -= distance
        else:
            raise RuntimeError(f"Unknown direction {direction}")
    path.append((x, y))
    return path


def get_intersection(p1, p2, p3, p4):
    """ Get the closet intersection to (0,0) of segments p1p2 and p3p4 if any """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    if x1 == x2:  # Segment p1p2 is vertical
        if x3 == x4:  # Segment p3p4 is vertical
            return None
        else:  # Segment p3p4 is horizontal
            assert (y3 == y4), "Segment should be either vertical or horizontal"
            y1, y2 = min(y1, y2), max(y1, y2)
            x3, x4 = min(x3, x4), max(x3, x4)
            if y1 <= y3 <= y2 and x3 <= x1 <= x4:
                return x1, y3
            else:
                return None
    else:  # Segment p1p2 is horizontal
        assert (y1 == y2)
        if x3 == x4:  # Segment p3p4 is vertical
            x1, x2 = min(x1, x2), max(x1, x2)
            y3, y4 = min(y3, y4), max(y3, y4)
            if x1 <= x3 <= x2 and y3 <= y1 <= y4:
                return x3, y1
            else:
                return None
        else:  # Segment p3p4 is horizontal
            assert (y3 == y4), "Segment should be either vertical or horizontal"
            return None


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        ans = solve(input_file)
        print(f"Intersection : {ans}, distance : {sum(map(abs, ans))}")

    p1, p2 = (100, 46), (155, 46)
    p3, p4 = (146, 53), (146, 4)
    print(get_intersection(p1, p2, p3, p4))
