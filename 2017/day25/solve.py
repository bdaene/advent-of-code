import re
from collections import defaultdict
from utils import timeit


@timeit
def get_data():

    start_pattern = re.compile(r'Begin in state (\w+)\.')
    steps_pattern = re.compile(r'Perform a diagnostic checksum after (\d+) steps\.')

    state_pattern = re.compile(r'In state (\w+):')
    rule_patterns = (
        re.compile(r'If the current value is (\d+):'),
        re.compile(r'- Write the value (\d+)\.'),
        re.compile(r'- Move one slot to the (\w+)\.'),
        re.compile(r'- Continue with state (\w+)\.'),
    )

    with open('input.txt') as input_file:
        start_state = start_pattern.search(input_file.readline()).group(1)
        nb_steps = int(steps_pattern.search(input_file.readline()).group(1))
        input_file.readline()

        states = {}
        for _ in range(6):
            state_name = state_pattern.search(input_file.readline()).group(1)
            rule0 = [pattern.search(input_file.readline()).group(1) for pattern in rule_patterns]
            assert rule0[0] == '0'
            rule1 = [pattern.search(input_file.readline()).group(1) for pattern in rule_patterns]
            assert rule1[0] == '1'
            input_file.readline()

            states[state_name] = {
                int(rule[0]): (int(rule[1]), -1 if rule[2] == 'left' else 1, rule[3])
                for rule in (rule0, rule1)}

    return start_state, nb_steps, states


@timeit
def part_1(data):

    start_state, nb_steps, states = data

    tape = defaultdict(int)
    cursor = 0
    current_state = start_state

    for _ in range(nb_steps):
        new_value, move, new_state = states[current_state][tape[cursor]]
        tape[cursor] = new_value
        cursor += move
        current_state = new_state

    return sum(tape.values())


@timeit
def part_2(data):
    return len(data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
