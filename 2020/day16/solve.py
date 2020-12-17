import re

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
    nb_fields = len(tickets[0])

    rules = {name: frozenset(range(a, b + 1)) | frozenset(range(c, d + 1)) for name, (a, b, c, d) in
             rules.items()}

    allowed_values = set()
    for rule, values in rules.items():
        allowed_values |= values
    valid_tickets = {ticket for ticket in tickets[1:] if all(value in allowed_values for value in ticket)}
    fields_values = [set(ticket[i] for ticket in valid_tickets) for i in range(nb_fields)]

    matching_fields = {
        name: set(field for field, field_values in enumerate(fields_values) if field_values <= rule_values)
        for name, rule_values in rules.items()}

    rules_field = {}
    rules = sorted(matching_fields, key=lambda r: len(matching_fields[r]))
    for i, rule in enumerate(rules):
        fields = matching_fields[rule]
        if len(fields) == 0:
            raise RuntimeError(f"No fields available for rule {rule}.")
        elif len(fields) == 1:
            field = fields.pop()
            rules_field[rule] = field
            for rule_ in rules[i + 1:]:
                matching_fields[rule_].discard(field)
        else:
            raise RuntimeError(f"Multiple possibilities for rule {rule}.")

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
