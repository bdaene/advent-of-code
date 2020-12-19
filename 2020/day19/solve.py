import re

from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        rules = {}
        for line in input_file:
            if line.isspace():
                break
            key, rule = line.split(': ')
            key = int(key)
            if rule.startswith('"'):
                rules[key] = rule[1]
            else:
                rule_or = rule.split(' | ')
                rules[key] = tuple(tuple(map(int, rule_a.split(' '))) for rule_a in rule_or)

        messages = [line.strip() for line in input_file]

    return rules, messages


def get_regex(rule, rules):
    if isinstance(rules[rule], str):
        return rules[rule]
    return '|'.join(
        f"(?:{''.join('(?:' + get_regex(rule_, rules) + ')' for rule_ in rule_a)})" for rule_a in rules[rule])


@timeit
def part_1(data):
    rules, messages = data
    pattern = re.compile(get_regex(0, rules))
    return sum(1 for message in messages if pattern.fullmatch(message))


@timeit
def part_2(data):
    rules, messages = data
    regex_42 = get_regex(42, rules)
    regex_31 = get_regex(31, rules)
    patterns = [re.compile(f"(?:{regex_42})+(?:{regex_42}){{{r}}}(?:{regex_31}){{{r}}}") for r in range(1, 5)]
    return sum(1 for message in messages if any(pattern.fullmatch(message) for pattern in patterns))


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
