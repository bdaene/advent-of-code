import re
from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import NamedTuple

from utils import timeit


@dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    tunnels: frozenset[str]


@timeit
def get_data():
    valves = {}
    pattern = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)')
    with open('input.txt') as input_file:
        for line in input_file:
            valve_name, flow_rate, tunnels = pattern.fullmatch(line.strip()).groups()
            valves[valve_name] = Valve(valve_name, int(flow_rate), frozenset(tunnels.split(', ')))
    return valves


def find_flow_valves(valves: dict[str, Valve], valve: str):
    queue = deque([(0, valve)])
    visited = set()
    while queue:
        distance, valve = queue.popleft()
        if valve in visited:
            continue
        visited.add(valve)

        if valves[valve].flow_rate > 0:
            yield distance, valve

        for v in valves[valve].tunnels:
            queue.append((distance + 1, v))


def get_graph(valves) -> dict[str, frozenset[tuple[int, str]]]:
    paths = {}
    for valve in valves:
        paths[valve] = frozenset(find_flow_valves(valves, valve))

    return paths


class State(NamedTuple):
    current_valves: frozenset[tuple[str, int]]
    open_valves: frozenset[str]
    open_flow: int
    closed_flow: int
    released_pressure: int

    def get_next_states(self, valves: dict[str, Valve], graph: dict[str: frozenset[tuple[int, str]]]):
        for current_valve, current_time in self.current_valves:
            for distance, valve in graph[current_valve]:
                if valve not in self.open_valves and current_time > distance:
                    yield State(
                        self.current_valves - {(current_valve, current_time)} | {(valve, current_time - distance - 1)},
                        self.open_valves | {valve},
                        self.open_flow + valves[valve].flow_rate,
                        self.closed_flow - valves[valve].flow_rate,
                        self.released_pressure + valves[valve].flow_rate * (current_time - distance - 1),
                    )


@timeit
def part_2(valves, time_limit=26):
    graph = get_graph(valves)
    print(graph)
    graph['AA_'] = graph['AA']

    start = State(
        current_valves=frozenset({('AA', time_limit), ('AA_', time_limit)}),
        open_valves=frozenset(),
        open_flow=0,
        closed_flow=sum(valve.flow_rate for valve in valves.values()),
        released_pressure=0,
    )

    def get_cost(state_):
        return (
            sum(time for valve, time in state_.current_valves),
            -state_.released_pressure,
        )

    heap: list[tuple[tuple, State]]
    heap = [(get_cost(start), start)]
    visited_state = set()

    best_pressure = 0

    while heap:
        _, state = heappop(heap)
        if state.released_pressure > best_pressure:
            best_pressure = state.released_pressure
            print(state)

        for next_state in state.get_next_states(valves, graph):
            if next_state in visited_state:
                continue
            visited_state.add(next_state)
            heappush(heap, (get_cost(next_state), next_state))


def main():
    valves = get_data()
    part_2(valves)


if __name__ == "__main__":
    main()
