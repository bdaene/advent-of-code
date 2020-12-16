import re
from collections import defaultdict

from utils import timeit


@timeit
def get_data():
    rules = {}
    rule_pattern = re.compile(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)')

    tickets = []
    with open('input.txt') as input_file:
        for line in input_file:
            if line.isspace():
                break
            name, *ranges = rule_pattern.fullmatch(line.strip()).groups()
            rules[name] = tuple(map(int, ranges))

        assert input_file.readline().strip() == 'your ticket:'
        tickets.append(tuple(map(int, input_file.readline().strip().split(','))))

        assert input_file.readline().isspace()
        assert input_file.readline().strip() == 'nearby tickets:'
        for line in input_file:
            if line.isspace():
                break
            tickets.append(tuple(map(int, line.strip().split(','))))

    return rules, tickets


@timeit
def part_1(data):
    rules, tickets = data
    allowed_values = set()
    for (a, b, c, d) in rules.values():
        allowed_values |= set(range(a, b + 1))
        allowed_values |= set(range(c, d + 1))

    total = 0
    for ticket in tickets[1:]:
        for value in ticket:
            if value not in allowed_values:
                total += value

    return total


@timeit
def part_2(data):
    rules, tickets = data

    valid_tickets = []
    for ticket in tickets:
        if all(any(a <= value <= b or c <= value <= d for a, b, c, d in rules.values()) for value in ticket):
            valid_tickets.append(ticket)

    fields_values = [set() for _ in tickets[0]]
    for ticket in valid_tickets:
        for i, value in enumerate(ticket):
            fields_values[i].add(value)

    matching_fields = defaultdict(set)
    for rule, (a, b, c, d) in rules.items():
        for field, values in enumerate(fields_values):
            if all(a <= value <= b or c <= value <= d for value in values):
                matching_fields[rule].add(field)

    rules_field = {}
    while len(matching_fields) > 0:
        for rule, fields in matching_fields.items():
            if len(fields) == 0:
                raise RuntimeError(f"No fields available for rule {rule}.")
            elif len(fields) == 1:
                field = fields.pop()
                del matching_fields[rule]
                rules_field[rule] = field
                for fields_ in matching_fields.values():
                    fields_.discard(field)
                break

    total = 1
    for rule, field in rules_field.items():
        if rule.startswith('departure'):
            total *= tickets[0][field]

    return total


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
