from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            value = line.strip()
            data.append(value)
    return data


@timeit
def part_1(data):
    count = [sum(map(int, bits)) for bits in zip(*data)]
    gamma_rate = int(''.join('1' if bits_count > len(data) - bits_count else '0' for bits_count in count), 2)
    epsilon_rate = int(''.join('1' if bits_count < len(data) - bits_count else '0' for bits_count in count), 2)
    return gamma_rate * epsilon_rate


class CountingTrie:

    def __init__(self):
        self._trie = {'count': 0}

    def add_entry(self, entry: str) -> None:
        node = self._trie

        for c in entry:
            node['count'] += 1
            if c not in node:
                node[c] = {'count': 0}
            node = node[c]

        node['$'] = entry

    def search(self, criterion) -> str:
        node = self._trie

        children = set(node) - {'count', '$'}
        while children:
            if len(children) > 1:
                node = node[criterion({child: node[child]['count'] for child in children})]
            else:
                node = node[children.pop()]
            children = set(node) - {'count', '$'}

        return node['$']


@timeit
def part_2(data):
    counting_trie = CountingTrie()
    for bits in data:
        counting_trie.add_entry(bits)

    oxygen_generator_rating = counting_trie.search(lambda children_count: '1' if children_count['1'] >= children_count['0'] else '0')
    co2_scrubber_rating = counting_trie.search(lambda children_count: '0' if children_count['0'] <= children_count['1'] else '1')

    return int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2)


def search(filter_function, data):
    numbers = set(data)
    i = 0
    while len(numbers) > 1:
        numbers_bit = {'0': set(), '1': set()}
        for number in numbers:
            numbers_bit[number[i]].add(number)

        numbers = filter_function(numbers_bit)
        i += 1

    return numbers.pop()


@timeit
def part_2_bis(data):
    def oxygen_generator_criteria(numbers_bit):
        return numbers_bit['1'] if len(numbers_bit['1']) >= len(numbers_bit['0']) else numbers_bit['0']

    def co2_scrubber_criteria(numbers_bit):
        return numbers_bit['0'] if len(numbers_bit['0']) <= len(numbers_bit['1']) else numbers_bit['1']

    oxygen_generator_rating = search(oxygen_generator_criteria, data)
    co2_scrubber_rating = search(co2_scrubber_criteria, data)

    return int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2)


def main():
    data = get_data()
    part_1(data)
    part_2(data)
    part_2_bis(data)


if __name__ == "__main__":
    main()
