from utils import timeit


@timeit
def get_data():
    replacements = []
    with open('input.txt') as input_file:
        for line in input_file:
            if line.isspace():
                break

            replacements.append(line.strip().split(' => '))

        return replacements, input_file.readline().strip()


@timeit
def part_1(data):
    replacements, molecule = data

    molecules = set()
    for a, b in replacements:
        for i in range(len(molecule) - len(a) + 1):
            if molecule[i:i + len(a)] == a:
                molecules.add(molecule[:i] + b + molecule[i + len(a):])

    return len(molecules)


@timeit
def part_2(data):
    replacements, molecule = data

    def reduce(molecule):
        for a, b in replacements:
            try:
                i = molecule.index(b)
                return molecule[:i] + a + molecule[i + len(b):]
            except ValueError:
                continue

    steps = 0
    while 'e' != molecule:
        steps += 1
        molecule = reduce(molecule)

    return steps


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
