from dataclasses import dataclass, field
from typing import Optional

from utils import timeit


@dataclass
class Node:
    name: str
    parent: Optional['Node'] = None
    size: Optional[int] = None


@dataclass
class Directory(Node):
    children: list['Node'] = field(default_factory=list)

    def compute_size(self):
        for child in self.children:
            if isinstance(child, Directory):
                child.compute_size()
        self.size = sum(child.size for child in self.children)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Directory):
                yield from child.walk()


@dataclass
class File(Node):
    pass


@timeit
def get_data():
    root = Directory('/')
    commands = []
    node = root
    with open('input.txt') as input_file:
        for line in input_file:
            line = line.strip()
            if line.startswith('$'):
                commands.append(line)
                if line == '$ ls':
                    pass
                elif line == '$ cd /':
                    node = root
                elif line == '$ cd ..':
                    node = node.parent
                else:
                    name = line.split()[-1]
                    node = next(n for n in node.children if n.name == name)
            else:
                if line.startswith('dir'):
                    name = line.removeprefix('dir ')
                    node.children.append(Directory(name, parent=node))
                else:
                    size, name = line.split()
                    node.children.append(File(name, parent=node, size=int(size)))
    return root, commands


@timeit
def part_1(root, limit=100000):
    root.compute_size()
    return sum(directory.size for directory in root.walk() if directory.size <= limit)


@timeit
def part_2(root, total_space=70000000, needed_space=30000000):
    root.compute_size()
    available_space = total_space - root.size
    space_to_delete = needed_space - available_space
    return min(directory.size for directory in root.walk() if directory.size >= space_to_delete)


def main():
    root, commands = get_data()
    part_1(root)
    part_2(root)


if __name__ == "__main__":
    main()
