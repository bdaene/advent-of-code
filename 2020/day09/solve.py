from utils import timeit


@timeit
def part_1(data, k=25):
    for i, s in enumerate(data[k:], k):
        if not any(s - a in data[j:i] for j, a in enumerate(data[i - k:i], i - k)):
            return s


@timeit
def part_1_bis(data, k=25):
    for i, s in enumerate(data[k:], k):
        seen, valid = set(), False
        for n in data[i - k:i]:
            if s - n in seen:
                valid = True
                break
            seen.add(n)
        if not valid:
            return s


@timeit
def part_2(data):
    target = part_1(data)

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if sum(data[i:j + 1]) == target:
                print(data[i:j + 1])
                print(min(data[i:j + 1]) + max(data[i:j + 1]))


@timeit
def part_2_bis(data):
    target = part_1_bis(data)

    i, j, s = 0, 2, sum(data[0:2])
    while j < len(data) or s > target:
        if s < target:
            s += data[j]
            j += 1
        elif s > target:
            s -= data[i]
            i += 1
        else:
            return min(data[i:j]) + max(data[i:j])


def main():
    with open('input.txt') as input_file:
        data = list(map(int, input_file.readlines()))

    print(data)
    part_1_bis(data)
    part_2_bis(data)


if __name__ == "__main__":
    main()
