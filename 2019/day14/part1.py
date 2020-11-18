
import re
from collections import defaultdict, Counter

PATTERN = re.compile(r'(.+) => (\d+ [A-Z]+)')


def solve(reactions):
    # print(reactions)
    output_inputs = defaultdict(dict)
    input_outputs = defaultdict(set)
    amount_produced = {'ORE': 1}

    for name, (amount, inputs) in reactions.items():
        amount_produced[name] = amount
        for input_amount, input_name in inputs:
            output_inputs[name][input_name] = input_amount
            input_outputs[input_name].add(name)

    quantities = Counter()
    quantities['FUEL'] = 1

    changed = set(output_inputs['FUEL'])

    while len(changed) > 0:
        name = changed.pop()
        needed_amount = 0
        for output_name in input_outputs[name]:
            needed_amount += (quantities[output_name]+amount_produced[output_name]-1) // amount_produced[output_name] * output_inputs[output_name][name]
        integer_amount = amount_produced[name]
        produced_amount = (needed_amount+integer_amount-1)//integer_amount*integer_amount
        if quantities[name] < produced_amount:
            quantities[name] = produced_amount
            changed |= set(output_inputs[name])

    return quantities['ORE']


def split_chemical(chemical):
    number, name = chemical.split(' ')
    return int(number), name


if __name__ == "__main__":
    reactions = defaultdict(tuple)
    with open('input.txt', 'r') as input_file:
        for line in input_file:
            input_chemicals, output_chemical = PATTERN.match(line).groups()
            output_number, output_name = split_chemical(output_chemical)
            if output_name in reactions:
                print(output_name)
            reactions[output_name] = (output_number, set(map(split_chemical, input_chemicals.split(', '))))
    print(solve(reactions))

