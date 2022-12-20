from dataclasses import dataclass
from typing import Iterable, Optional

from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(int(value))
    return data


@dataclass
class Node:
    value: int
    left: 'Node' = None
    right: 'Node' = None

    def __post_init__(self):
        if self.left is None:
            self.left = self
        if self.right is None:
            self.right = self

    def insert_left(self, node):
        node.left.right, node.left, self.right.left, self.right = self.right, self, node.left, node

    def insert_right(self, node):
        node.right.left, node.right, self.left.right, self.left = self.left, self, node.right, node

    def detach(self):
        self.left.right, self.right.left = self.right, self.left
        self.left, self.right = self, self


class CircularList:
    def __init__(self, values: Iterable[int] = ()):
        self.last_node: Optional[Node] = None
        self.nodes = []
        for value in values:
            self.add_value(value)

    def add_value(self, value: int):
        node = Node(value)
        self.nodes.append(node)

        if self.last_node is not None:
            node.insert_right(self.last_node)
        self.last_node = node
        return node

    def to_list(self, start=None):
        if start is None:
            start = self.last_node

        result, node = [], start
        for _ in range(len(self.nodes)):
            result.append(node.value)
            node = node.right
        return result

    def move(self, node):
        value = node.value
        steps = value % (len(self.nodes) - 1)
        if steps == 0:
            return
        current = node
        while steps > 0:
            current = current.right
            steps -= 1
        node.detach()
        node.insert_right(current)


@timeit
def part_1(data, rounds=1):
    circular_list = CircularList(data)

    for r in range(rounds):
        for node in circular_list.nodes:
            circular_list.move(node)
        print(r + 1, circular_list.to_list())

    zero_node = next(node for node in circular_list.nodes if node.value == 0)
    values = circular_list.to_list(zero_node)
    return sum(values[i * 1000 % len(values)] for i in range(1, 4))


@timeit
def part_2(data):
    data = [d * 811589153 for d in data]
    return part_1.func(data, rounds=10)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
