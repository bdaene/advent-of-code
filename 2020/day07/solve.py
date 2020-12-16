import re
from collections import defaultdict

from utils import timeit


@timeit
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

    return len(seen_bags) - 1


@timeit
def part_2(bags):
    def size(out_bag):
        return sum(count * (1 + size(in_bag)) for count, in_bag in bags[out_bag])

    return size(('shiny', 'gold'))


@timeit
def scan_bags(input_file):
    bags = {}
    bag_pattern = re.compile(r'(\d+ )?(\w+) (\w+) bags?')
    for line in input_file:
        out_bag, in_bags = line.strip().split(' contain ')
        if in_bags == 'no other bags.':
            in_bags = []
        else:
            in_bags = in_bags[:-1].split(', ')

        count, modifier, color = bag_pattern.fullmatch(out_bag).groups()
        out_bag = (modifier, color)
        assert out_bag not in bags
        bags[out_bag] = []
        for in_bag in in_bags:
            count, modifier, color = bag_pattern.fullmatch(in_bag).groups()
            bags[out_bag].append((int(count), (modifier, color)))

    return bags


def main():
    with open('input.txt') as input_file:
        bags = scan_bags(input_file)

    part_1(bags)
    part_2(bags)


if __name__ == "__main__":
    main()
