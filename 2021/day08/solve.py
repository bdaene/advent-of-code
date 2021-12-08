from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            digits, number = line.split(' | ')
            digits = frozenset(map(frozenset, digits.split()))
            number = tuple(map(frozenset, number.split()))

            data.append((digits, number))
    return data


@timeit
def part_1(data):
    return sum(len(digit) in (2, 4, 3, 7) for _, number in data for digit in number)


def get_mapping(digits):
    segments_count = {}
    for segments in digits:
        count = len(segments)
        if count not in segments_count:
            segments_count[count] = {segments}
        else:
            segments_count[count].add(segments)

    """
     aaaa 
    b    c
    b    c
     dddd 
    e    f
    e    f
     gggg
      
        abcdefg
    1     *  *
    4    *** *
    7   * *  * 
    8   *******
    2   * *** *
    5   ** * **
    3   * ** **
    6   ** ****
    0   *** ***
    9   **** ** 
    """

    digit_1, digit_4, digit_7, digit_8 = (segments_count[d].pop() for d in (2, 4, 3, 7))
    digit_2, digit_5, digit_3 = sorted(segments_count[5], key=lambda d: (len(d & digit_1), len(d & digit_4)))
    digit_6, digit_0, digit_9 = sorted(segments_count[6], key=lambda d: (len(d & digit_1), len(d & digit_4)))

    return {segments: f'{digit}' for digit, segments in enumerate((
        digit_0, digit_1, digit_2, digit_3, digit_4, digit_5, digit_6, digit_7, digit_8, digit_9
    ))}


@timeit
def part_2(data):

    total = 0
    for digits, number in data:
        mapping = get_mapping(digits)
        total += int(''.join(mapping[segments] for segments in number))
    return total


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
