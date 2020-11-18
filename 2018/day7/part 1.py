
from collections import defaultdict
import re
from heapq import heappush, heappop


PATTERN = re.compile(r'Step (.*) must be finished before step (.*) can begin.')
NB_WORKERS = 5
BASIC_STEP_TIME = 60


def solve(input_file):
    parents = defaultdict(set)
    children = defaultdict(set)
    for line in input_file:
        step_a, step_b = PATTERN.match(line).groups()
        parents[step_b].add(step_a)
        children[step_a].add(step_b)

    available = set(step for step in children if step not in parents)
    time_of_completion = {}
    ongoing_steps = []
    workers = 0
    while available and workers < NB_WORKERS:
        current_step = min(available)
        available.remove(current_step)
        heappush(ongoing_steps, (BASIC_STEP_TIME+ord(current_step)-ord('A')+1, current_step))
        workers += 1

    while ongoing_steps:
        time, current_step = heappop(ongoing_steps)
        time_of_completion[current_step] = time
        print(f"{time:4} : {current_step}")
        workers -= 1

        for next_step in children[current_step]:
            if len(parents[next_step] - time_of_completion.keys()) == 0:
                available.add(next_step)

        while available and workers < NB_WORKERS:
            next_step = min(available)
            available.remove(next_step)
            heappush(ongoing_steps, (time + BASIC_STEP_TIME + ord(next_step) - ord('A') + 1, next_step))
            workers += 1

    return max(time_of_completion.values())


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
