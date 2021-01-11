from utils import timeit


@timeit
def get_packages():
    with open('input.txt') as input_file:
        return tuple(int(line) for line in input_file)


def gen_group(weight, packages):
    if weight < 0:
        return
    elif weight == 0:
        yield frozenset()
    elif len(packages) > 0:
        package, *_ = packages
        yield from gen_group(weight, packages - {package})
        for group in gen_group(weight - package, packages - {package}):
            yield group | {package}


@timeit
def part_1(packages):
    target = sum(packages) // 3
    packages = frozenset(packages)
    best = (len(packages), sum(packages) ** len(packages))
    for front_packages in gen_group(target, packages):
        if len(front_packages) > best[0]:
            continue
        quantum_entanglement = 1
        for package in front_packages:
            quantum_entanglement *= package
        if quantum_entanglement < best[1]:
            try:
                next(gen_group(target, packages - front_packages))
                best = (len(front_packages), quantum_entanglement)
            except StopIteration:
                continue

        print(best)

    return best[1]


@timeit
def part_2(packages):
    target = sum(packages) // 4
    packages = frozenset(packages)
    best = (len(packages), sum(packages) ** len(packages))
    for front_packages in gen_group(target, packages):
        if len(front_packages) > best[0]:
            continue
        quantum_entanglement = 1
        for package in front_packages:
            quantum_entanglement *= package
        if quantum_entanglement < best[1]:
            try:
                trunk_packages = next(gen_group(target, packages - front_packages))
                next(gen_group(target, packages - front_packages - trunk_packages))
                best = (len(front_packages), quantum_entanglement)
            except StopIteration:
                continue

        print(best)

    return best[1]


def main():
    packages = get_packages()
    part_1(packages)
    part_2(packages)


if __name__ == "__main__":
    main()
