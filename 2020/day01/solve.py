from utils import timeit


@timeit
def part_1(data):
    for i, expense in enumerate(data):
        expense_2 = 2020 - expense
        if expense_2 in data[i + 1:]:
            return expense * expense_2


@timeit
def part_2(data):
    for i, expense_1 in enumerate(data):
        for j, expense_2 in enumerate(data[i + 1:], i + 1):
            expense_3 = 2020 - expense_1 - expense_2
            if expense_3 in data[j + 1:]:
                return expense_1 * expense_2 * expense_3


def main():
    with open('input.txt') as input_file:
        data = [int(entry) for entry in input_file]

    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
