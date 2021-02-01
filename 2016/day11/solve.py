import re
from itertools import combinations
from heapq import heappush, heappop
from utils import timeit


@timeit
def get_data():
    data = []
    generator_pattern = re.compile(r'a (\w+) generator')
    microchip_pattern = re.compile(r'a (\w+)-compatible microchip')
    with open('input.txt') as input_file:
        for line in input_file:
            generators = set(match.group(1) for match in re.finditer(generator_pattern, line))
            microchips = set(match.group(1) for match in re.finditer(microchip_pattern, line))
            data.append((generators, microchips))
    return data


def is_valid(floors):
    for generator, microchip in floors:
        if generator != microchip:
            if any(generator_ == microchip for generator_, microchip_ in floors):
                return False
    return True


def gen_next_states(state):
    nb_moves, elevator, floors, moves = state
    objects = tuple((e, t) for e, element in enumerate(floors) for t in (0, 1) if element[t] == elevator)

    for d in (+1, -1):
        if not 0 <= elevator + d <= 3:
            continue
        for c in (1, 2):
            for taken_objects in combinations(objects, c):
                floors_ = list(list(element) for element in floors)
                for element, t in taken_objects:
                    floors_[element][t] = elevator + d
                floors_ = tuple(tuple(element) for element in floors_)
                if is_valid(floors_):
                    yield nb_moves + 1, elevator + d, floors_, moves + ((elevator, floors),)


@timeit
def part_1(data):

    elements = []
    for generators, microchips in data:
        elements.extend(generators)
    elements = tuple(sorted(elements))
    print(elements)

    floors = tuple([None, None] for _ in elements)
    for f, (generators, microchips) in enumerate(data):
        for generator in generators:
            floors[elements.index(generator)][0] = f
        for microchip in microchips:
            floors[elements.index(microchip)][1] = f
    floors = tuple(tuple(element) for element in floors)

    heap = [(0, 0, floors, ())]
    seen = set()
    while heap:
        state = heappop(heap)
        nb_moves, elevator, floors, moves = state
        if all(element[t] == 3 for element in floors for t in (0, 1)):
            return nb_moves, moves

        for state_ in gen_next_states(state):
            key = (state_[1], tuple(sorted(state_[2])))
            if key not in seen:
                seen.add(key)
                heappush(heap, state_)


@timeit
def part_2(data):
    data[0][0].update({'elerium', 'dilithium'})
    data[0][1].update({'elerium', 'dilithium'})

    return part_1.func(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
