from utils import timeit


def look_and_say(digits):
    prev, count = digits[0], 1
    new_digits = []
    for d in digits[1:]:
        if d == prev:
            count += 1
        else:
            new_digits.append(f"{count}")
            new_digits.append(prev)
            prev = d
            count = 1
    new_digits.append(f"{count}")
    new_digits.append(prev)

    return ''.join(new_digits)


@timeit
def part_1(digits='3113322113', times=40):
    for _ in range(times):
        digits = look_and_say(digits)
    return len(digits)


@timeit
def part_2():
    return part_1.func(times=50)


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
