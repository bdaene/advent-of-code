import re
from collections import defaultdict


def part_1(bags):
    parents = defaultdict(set)
    for out_bag, other_bags in bags.items():
        for count, in_bag in other_bags:
            parents[in_bag].add(out_bag)

    stack = [('shiny', 'gold')]
    seen_bags = set()
    while stack:
        in_bag = stack.pop()
        seen_bags.add(in_bag)
        for out_bag in parents[in_bag]:
            if out_bag not in seen_bags:
                stack.append(out_bag)

    print(len(seen_bags) - 1)


def part_2(bags):
    stack = [('shiny', 'gold')]
    seen_bags = {}
    while stack:
        out_bag = stack.pop()
        if out_bag in seen_bags:
            if seen_bags[out_bag] is None:
                seen_bags[out_bag] = sum(count * (1 + seen_bags[in_bag]) for count, in_bag in bags[out_bag])
        else:
            seen_bags[out_bag] = None
            stack.append(out_bag)
            for count, in_bag in bags[out_bag]:
                stack.append(in_bag)

    print(seen_bags[('shiny', 'gold')])


def scan_bags(input_file):
    bags = {}
    bag_pattern = re.compile(r'(\d+ )?(\w+) (\w+) bags?')
    for line in input_file:
        bag, other_bags = line.strip().split(' contain ')
        if other_bags == 'no other bags.':
            other_bags = []
        else:
            other_bags = other_bags[:-1].split(', ')

        count, modifier, color = bag_pattern.fullmatch(bag).groups()
        key = (modifier, color)
        assert key not in bags
        bags[key] = []
        for bag in other_bags:
            count, modifier, color = bag_pattern.fullmatch(bag).groups()
            bags[key].append((int(count), (modifier, color)))

    return bags


def main():
    with open('input.txt') as input_file:
        bags = scan_bags(input_file)

    print(bags)
    part_1(bags)
    part_2(bags)


if __name__ == "__main__":
    main()
