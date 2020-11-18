

from collections import Counter


def solve(input_file):
    box_ids = input_file.read().splitlines()
    for i, box_a in enumerate(box_ids):
        for box_b in box_ids[i+1:]:
            if sum(1 for a, b in zip(box_a, box_b) if a != b) <= 1:
                return ''.join(a for a, b in zip(box_a, box_b) if a == b)


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))