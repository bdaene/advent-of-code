def part_1(answers):
    total = 0
    for group in answers:
        group_answer = set(group[0])
        for answer in group[1:]:
            group_answer |= set(answer)
        total += len(group_answer)
    print(total)


def part_2(answers):
    total = 0
    for group in answers:
        group_answer = set(group[0])
        for answer in group[1:]:
            group_answer &= set(answer)
        total += len(group_answer)
    print(total)


def scan_answers(input_file):
    group = []
    for line in input_file:
        if line.isspace():
            yield group
            group = []
        else:
            group.append(line.strip())
    yield group


def main():
    with open('input.txt') as input_file:
        answers = list(scan_answers(input_file))

    print(answers)
    part_1(answers)
    part_2(answers)


if __name__ == "__main__":
    main()
