import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from itertools import product
from typing import TypeVar

from utils import timeit

ValveName = TypeVar('ValveName', bound=str)


@dataclass(frozen=True)
class Valve:
    flow_rate: int
    tunnels: frozenset[str]


@timeit
def get_data():
    valves = {}
    pattern = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)')
    with open('input.txt') as input_file:
        for line in input_file:
            valve_name, flow_rate, valve_tunnels = pattern.fullmatch(line.strip()).groups()
            valves[valve_name] = Valve(int(flow_rate), frozenset(valve_tunnels.split(', ')))
    return valves


def get_distances(valves: dict[ValveName, Valve]):
    distances = defaultdict(lambda: len(valves))
    for valve_name, valve in valves.items():
        for tunnel in valve.tunnels:
            distances[valve_name, tunnel] = 1

    for k, i, j in product(valves, repeat=3):
        distances[i, j] = min(distances[i, j], distances[i, k] + distances[k, j])

    destinations = {valve_name for valve_name, valve in valves.items() if valve.flow_rate > 0}
    return {valve_name: {destination_name: distances[valve_name, destination_name]
                         for destination_name in destinations}
            for valve_name in valves}


@timeit
def part_1(valves, time_limit=30, start_valve='AA', nb_agents=1):
    distances = get_distances(valves)
    closed_valves = frozenset(valve_name for valve_name, valve in valves.items() if valve.flow_rate > 0)
    distance_to_closed = {valve_name: {name: distances[valve_name][name]
                                       for name in closed_valves}
                          for valve_name in valves}

    @cache
    def get_max_pressure(remaining_agents: int = nb_agents, remaining_time: int = time_limit,
                         current_valve_name: ValveName = start_valve,
                         remaining_valves: frozenset[ValveName] = closed_valves) -> int:

        available_valves = {valve: time
                            for valve in remaining_valves
                            if (time := remaining_time - distance_to_closed[current_valve_name][valve] - 1) > 0}
        best = 0
        if available_valves:
            best = max(valves[valve].flow_rate * time +
                       get_max_pressure(remaining_agents, time, valve, remaining_valves - {valve})
                       for valve, time in available_valves.items())

        if remaining_agents > 1:
            best = max(best, get_max_pressure(remaining_agents=remaining_agents - 1, remaining_valves=remaining_valves))

        return best

    return get_max_pressure()


@timeit
def part_2(valves):
    return part_1.func(valves, nb_agents=2, time_limit=26)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
