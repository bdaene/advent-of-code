import re
from utils import timeit


bot_pattern = re.compile(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')
value_pattern = re.compile(r'value (\d+) goes to bot (\d+)')


@timeit
def get_data():
    bots = {}
    values = []
    with open('input.txt') as input_file:
        for line in input_file:
            if match := bot_pattern.match(line):
                bot_key, low_type, low_key, high_type, high_key = match.groups()
                bots[int(bot_key)] = ((low_type, int(low_key)), (high_type, int(high_key)))
            elif match := value_pattern.match(line):
                value_key, bot_key = match.groups()
                values.append((int(value_key), int(bot_key)))
            else:
                raise ValueError(f"Could not parse: '{line}'")
    return bots, values


@timeit
def part_1(data):
    bots, values = data

    bots_values = {}

    def give(value, bot):
        if bot in bots_values:
            value_ = bots_values.pop(bot)
            value, value_ = sorted((value, value_))
            if (value, value_) == (17, 61):
                print(bot)
            (low_type, low_key), (high_type, high_key) = bots[bot]
            if low_type == 'bot':
                give(value, low_key)
            if high_type == 'bot':
                give(value_, high_key)
        else:
            bots_values[bot] = value

    for value_key, bot_key in values:
        give(value_key, bot_key)


@timeit
def part_2(data):
    bots, values = data

    bots_values = {}
    output_values = {}

    def give(value, bot):
        if bot in bots_values:
            value_ = bots_values.pop(bot)
            value, value_ = sorted((value, value_))
            (low_type, low_key), (high_type, high_key) = bots[bot]
            if low_type == 'bot':
                give(value, low_key)
            else:
                output_values[low_key] = value
            if high_type == 'bot':
                give(value_, high_key)
            else:
                output_values[high_key] = value_
        else:
            bots_values[bot] = value

    for value_key, bot_key in values:
        give(value_key, bot_key)

    return output_values[0] * output_values[1] * output_values[2]


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
