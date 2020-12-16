from utils import timeit


@timeit
def part_1(answers):
    total = 0
    for group in answers:
        group_answer = set(group[0])
        for answer in group[1:]:
            group_answer |= set(answer)
        total += len(group_answer)
    return total


@timeit
def part_2(answers):
    total = 0
    for group in answers:
        group_answer = set(group[0])
        for answer in group[1:]:
            group_answer &= set(answer)
        total += len(group_answer)
    return total


@timeit
def scan_answers(input_file):
    groups = []
    group = []
    for line in input_file:
        if line.isspace():
            groups.append(group)
            group = []
        else:
            group.append(line.strip())
    groups.append(group)
    return groups


def main():
    with open('input.txt') as input_file:
        answers = scan_answers(input_file)

    part_1(answers)
    part_2(answers)


if __name__ == "__main__":
    main()
