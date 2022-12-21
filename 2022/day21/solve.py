from copy import deepcopy
from dataclasses import dataclass

from sympy import Symbol, solve
from utils import timeit


@dataclass
class Monkey:
    value: int = None
    operation: str = None
    left: str = None
    right: str = None


@timeit
def get_data():
    monkeys = {}
    with open('input.txt') as input_file:
        for line in input_file:
            name, value = line.split(':')
            try:
                value = int(value)
                monkey = Monkey(value=value)
            except ValueError:
                left, operation, right = value.split()
                monkey = Monkey(left=left, right=right, operation=operation)

            monkeys[name] = monkey
    return monkeys


def resolve(monkeys, root='root'):
    stack = [root]

    while stack:
        monkey_name = stack.pop()
        monkey = monkeys[monkey_name]
        if monkey.value is not None:
            continue
        left, right = monkeys[monkey.left].value, monkeys[monkey.right].value
        if left is None or right is None:
            stack.append(monkey_name)
            if left is None:
                stack.append(monkey.left)
            if right is None:
                stack.append(monkey.right)
            continue
        if monkey.operation == '+':
            monkey.value = left + right
        elif monkey.operation == '-':
            monkey.value = left - right
        elif monkey.operation == '*':
            monkey.value = left * right
        elif monkey.operation == '/':
            monkey.value = left / right


@timeit
def part_1(monkeys):
    monkeys = deepcopy(monkeys)
    resolve(monkeys, 'root')

    return int(monkeys['root'].value)


@timeit
def part_2(monkeys):
    monkeys = deepcopy(monkeys)
    monkeys['root'].operation = '-'
    monkeys['humn'].value = x = Symbol('x')

    resolve(monkeys, 'root')
    expr = monkeys['root'].value

    return int(solve(expr, x)[0])


def main():
    monkeys = get_data()
    part_1(monkeys)
    part_2(monkeys)


if __name__ == "__main__":
    main()
