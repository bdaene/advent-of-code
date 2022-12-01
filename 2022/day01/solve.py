from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        elf = []
        for line in input_file:
            if line.isspace():
                data.append(elf)
                elf = []
            else:
                elf.append(int(line.strip()))
        data.append(elf)
    return data


@timeit
def part_1(data):
    return max(map(sum, data))


@timeit
def part_2(data):
    return sum(sorted(map(sum, data), reverse=True)[:3])


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
