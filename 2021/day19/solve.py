from itertools import combinations

from utils import timeit, DisjointSets


@timeit
def get_data():
    scanners = []
    with open('input.txt') as input_file:
        while True:
            input_file.readline()  # Scanner header
            scanners.append([])
            for line in input_file:
                if line.isspace():
                    break
                scanners[-1].append(tuple(map(int, line.split(','))))
            if not line.isspace():
                break
    return tuple(map(tuple, scanners))


def get_dist_2(a, b):
    return sum((a_x - b_x) ** 2 for a_x, b_x in zip(a, b))


def get_signature(scanner):
    return {i: set(get_dist_2(a, b) for b in scanner) for i, a in enumerate(scanner)}


def match(signature_a, signature_b):
    for a, sign_a in signature_a.items():
        for b, sign_b in signature_b.items():
            if len(sign_a & sign_b) >= 12:
                yield a, b
                break


PERMUTATIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (z, x, y),
]

ROTATIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (x, -z, y),

    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (-x, z, y),
]


def get_translation(a, b):
    dx, dy, dz = (b_x - a_x for a_x, b_x in zip(a, b))
    return lambda x, y, z: (x + dx, y + dy, z + dz)


@timeit
def part_1(data):
    signatures = {i: get_signature(scanner) for i, scanner in enumerate(data)}

    scanners = {0: data[0]}
    new_scanners = [0]
    while new_scanners:
        origin_scanner = new_scanners.pop()
        for scanner, signature in signatures.items():
            if scanner in scanners:
                continue
            matches = list(match(signatures[origin_scanner], signature))
            if not matches:
                continue
            original_beacons = list(scanners[origin_scanner][a] for a, b in matches)
            beacons = list(data[scanner][b] for a, b in matches)
            for permutation in PERMUTATIONS:
                for rotation in ROTATIONS:
                    translation = get_translation(rotation(*permutation(*beacons[0])), original_beacons[0])
                    if all(translation(*rotation(*permutation(*b))) == a for a, b in zip(original_beacons, beacons)):
                        scanners[scanner] = tuple(translation(*rotation(*permutation(*b))) for b in data[scanner])
                        new_scanners.append(scanner)

    all_beacons = set(beacon for beacons in scanners.values() for beacon in beacons)

    return len(all_beacons)


@timeit
def part_2(data):
    signatures = {i: get_signature(scanner) for i, scanner in enumerate(data)}

    scanners = {0: data[0]}
    scanners_position = {0: (0, 0, 0)}
    new_scanners = [0]
    while new_scanners:
        origin_scanner = new_scanners.pop()
        for scanner, signature in signatures.items():
            if scanner in scanners:
                continue
            matches = list(match(signatures[origin_scanner], signature))
            if not matches:
                continue
            original_beacons = list(scanners[origin_scanner][a] for a, b in matches)
            beacons = list(data[scanner][b] for a, b in matches)
            for permutation in PERMUTATIONS:
                for rotation in ROTATIONS:
                    translation = get_translation(rotation(*permutation(*beacons[0])), original_beacons[0])
                    if all(translation(*rotation(*permutation(*b))) == a for a, b in zip(original_beacons, beacons)):
                        scanners[scanner] = tuple(translation(*rotation(*permutation(*b))) for b in data[scanner])
                        scanners_position[scanner] = translation(*rotation(*permutation(*(0, 0, 0))))
                        new_scanners.append(scanner)

    return max(sum(abs(a_x - b_x) for a_x, b_x in zip(a, b)) for a, b in combinations(scanners_position.values(), 2))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
