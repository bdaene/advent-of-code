
from collections import defaultdict


def solve(input_file):
    data = tuple(map(int, input_file.readline().strip().split()))
    # data = tuple(map(int, "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split()))

    tree_data = {}
    tree_children = defaultdict(list)
    tree_value = {}

    def extract_data(index):
        nb_children = data[index]
        nb_data = data[index + 1]
        child_index = index + 2
        for child in range(nb_children):
            tree_children[index].append(child_index)
            child_index = extract_data(child_index)
        tree_data[index] = data[child_index:child_index+nb_data]

        if len(tree_children[index]) == 0:
            tree_value[index] = sum(tree_data[index])
        else:
            tree_value[index] = 0
            for i in tree_data[index]:
                if 0 < i <= len(tree_children[index]):
                    tree_value[index] += tree_value[tree_children[index][i-1]]

        return child_index+nb_data

    extract_data(0)

    return tree_value[0]


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
