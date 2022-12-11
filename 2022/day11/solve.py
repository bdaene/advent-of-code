import re
from copy import deepcopy
from dataclasses import dataclass
from math import gcd

from utils import timeit


@dataclass
class Monkey:
    index: int
    items: list[int]
    operation: str
    divisibility_test: int
    monkey_if_true: int
    monkey_if_false: int
    items_inspected: int = 0


@timeit
def get_data():
    data = {}
    with open('input.txt') as input_file:
        for line in input_file:
            monkey = Monkey(
                index=int(re.fullmatch(r'Monkey (\d+):', line.strip()).group(1)),
                items=list(map(int, input_file.readline().strip().split(': ')[-1].split(', '))),
                operation=input_file.readline().strip().split(' = ')[-1],
                divisibility_test=int(
                    re.fullmatch(r'Test: divisible by (\d+)', input_file.readline().strip()).group(1)),
                monkey_if_true=int(
                    re.fullmatch(r'If true: throw to monkey (\d+)', input_file.readline().strip()).group(1)),
                monkey_if_false=int(
                    re.fullmatch(r'If false: throw to monkey (\d+)', input_file.readline().strip()).group(1)),
            )
            input_file.readline()
            data[monkey.index] = monkey
    return data


@timeit
def part_1(monkeys, nb_rounds=20, worry_relief=3):
    monkeys = deepcopy(monkeys)
    worry_modulo = 1
    for monkey in monkeys.values():
        worry_modulo *= monkey.divisibility_test // gcd(worry_modulo, monkey.divisibility_test)

    for _ in range(nb_rounds):
        for monkey in monkeys.values():
            for item in monkey.items:
                item = eval(monkey.operation, dict(old=item)) // worry_relief % worry_modulo
                if item % monkey.divisibility_test == 0:
                    monkeys[monkey.monkey_if_true].items.append(item)
                else:
                    monkeys[monkey.monkey_if_false].items.append(item)
            monkey.items_inspected += len(monkey.items)
            monkey.items.clear()

    a, b = sorted(monkey.items_inspected for monkey in monkeys.values())[-2:]
    return a * b


@timeit
def part_2(monkeys):
    return part_1.func(monkeys, nb_rounds=10000, worry_relief=1)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
