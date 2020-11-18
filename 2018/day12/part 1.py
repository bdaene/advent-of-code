
import re
from collections import defaultdict

PATTERN_INITIAL = re.compile(r'initial state:\s*([\.#]*)')
PATTERN_RULE = re.compile(r'([\.#]{5})\s*=>\s*([\.#])')


def solve(input_file):
    initial_state = PATTERN_INITIAL.match(input_file.readline()).group(1)
    input_file.readline()
    rules = {}
    for line in input_file:
        llcrr, n = PATTERN_RULE.match(line).groups()
        rules[tuple(llcrr)] = n

    current_state = defaultdict(lambda: '.')
    for i, state in enumerate(initial_state):
        current_state[i] = state

    changed = set(range(-2, len(initial_state) + 2))
    for generation in range(100000):
        new_state = {}
        for pot in changed:
            states = tuple(current_state[i] for i in range(pot-5, pot))
            for i in range(pot - 2, pot + 3):
                states = states[1:] + (current_state[i+2],)
                new_state[i] = rules[states]

        changed = set()
        for pot, state in new_state.items():
            if state != current_state[pot]:
                changed.add(pot)
                current_state[pot] = state

        if generation % 1000 == 999:
            print(generation,':', len(changed), ':', sum(pot for pot, state in current_state.items() if state == '#'))
            # print(''.join(current_state[pot] for pot in range(min(changed), max(changed)+1)))

    return sum(pot for pot, state in current_state.items() if state == '#')


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
