import re
from collections import defaultdict

from utils import timeit


@timeit
def get_instructions():
    instructions = []
    with open('input.txt') as input_file:
        for line in input_file:
            operation, wire = line.strip().split(' -> ')
            instructions.append((operation.split(), wire))
    return tuple(instructions)


wire_ids = re.compile(r'[a-z]+')


def get_needed_wires(operation):
    return frozenset(op for op in operation if wire_ids.match(op))


def get_result(operation, wires):
    if len(operation) == 1:
        a = operation[0]
        return wires[a] if wire_ids.match(a) else int(a)

    if operation[0] == 'NOT':
        return ~ wires[operation[1]]

    a, op, b = operation
    a = wires[a] if wire_ids.match(a) else int(a)
    b = wires[b] if wire_ids.match(b) else int(b)

    if op == 'OR':
        return a | b
    if op == 'AND':
        return a & b
    if op == 'LSHIFT':
        return a << b
    if op == 'RSHIFT':
        return a >> b

    raise RuntimeError(f"Unknown {operation=}.")


@timeit
def part_1(instructions, set_wires=None):
    wires = {}
    if set_wires is not None:
        wires.update(set_wires)

    instructions = list(instructions)
    waiting_wires = defaultdict(list)

    while len(instructions) > 0:
        operation, wire = instructions.pop()
        if wire in wires:
            continue

        missing_wires = get_needed_wires(operation) - wires.keys()
        if len(missing_wires) > 0:
            for wire_ in missing_wires:
                waiting_wires[wire_].append((operation, wire))
        else:
            wires[wire] = get_result(operation, wires)
            instructions.extend(waiting_wires[wire])

    return wires['a']


@timeit
def part_2(instructions):
    a = part_1.func(instructions)
    return part_1.func(instructions, {'b': a})


def main():
    instructions = get_instructions()
    part_1(instructions)
    part_2(instructions)


if __name__ == "__main__":
    main()
