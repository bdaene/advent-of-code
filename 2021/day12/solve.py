from functools import cache
from utils import timeit


@timeit
def get_data():
    data = {}
    with open('input.txt') as input_file:
        for line in input_file:
            a, b = line.strip().split('-')
            if a not in data:
                data[a] = set()
            data[a].add(b)
            if b not in data:
                data[b] = set()
            data[b].add(a)
    return data


@timeit
def part_1(data):

    @cache
    def count_paths(node, visited_nodes=frozenset()):
        if node == 'end':
            return 1
        else:
            if node == node.lower():
                visited_nodes |= {node}
            return sum(count_paths(next_node, visited_nodes) for next_node in data[node] - visited_nodes)

    return count_paths('start')


@timeit
def part_2(data):

    @cache
    def count_paths(node, visited_nodes=frozenset(), double_visit_done=False):
        if node == 'end':
            return 1
        else:
            if node == node.lower():
                if node in visited_nodes:
                    double_visit_done = True
                visited_nodes |= {node}

            next_nodes = data[node] - visited_nodes if double_visit_done else data[node] - {'start'}
            return sum(count_paths(next_node, visited_nodes, double_visit_done) for next_node in next_nodes)

    return count_paths('start')


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
