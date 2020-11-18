
from collections import defaultdict


def solve(input_file):
    orbits = defaultdict(set)
    parent = {}
    for line in input_file:
        a, b = line.strip().split(')')
        orbits[a].add(b)
        parent[b] = a
    distance = {}
    stack = [('COM', 0)]
    while stack:
        planet, dist = stack.pop()
        distance[planet] = dist
        for moon in orbits[planet]:
            stack.append((moon, dist + 1))

    santa, you, count = 'SAN', 'YOU', 0
    while parent[santa] != parent[you]:
        if distance[santa] > distance[you]:
            santa = parent[santa]
        else:
            you = parent[you]
        count += 1

    return count


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))