import re
from time import perf_counter


def timeit(func):
    def wrapper(*args, **kwargs):
        clock = perf_counter()
        result = func(*args, **kwargs)
        print(f"Execution of {func.__name__} took {(perf_counter() - clock) * 1000:.3f}ms.")
        print(f"Result: {result}")
        return result

    return wrapper


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            if line.startswith('mask'):
                mask = re.fullmatch(r'mask = ([01X]+)', line.strip()).group(1)
                data.append(('mask', mask))
            else:
                address, value = re.fullmatch(r'mem\[(\d+)\] = (\d+)', line.strip()).groups()
                data.append(('mem', int(address), int(value)))
    return data


@timeit
def part_1(data):
    mask_or = 0
    mask_and = (1 << 36) - 1
    memory = {}

    for action in data:
        if action[0] == 'mask':
            mask = action[1]
            mask_or = int(mask.replace('X', '0'), 2)
            mask_and = int(mask.replace('X', '1'), 2)
        elif action[0] == 'mem':
            address, value = action[1:]
            memory[address] = (value | mask_or) & mask_and
        else:
            raise RuntimeError("Unknown action")

    return sum(memory.values())


@timeit
def part_2(data):
    memory = {}
    mask = 0

    def gen_addresses(address, mask):
        if len(mask) == 0:
            yield address
            return
        if mask[0] == '0':
            yield from gen_addresses(address, mask[1:])
        elif mask[0] == '1':
            yield from gen_addresses(address | (1 << (len(mask) - 1)), mask[1:])
        else:
            yield from gen_addresses(address | (1 << (len(mask) - 1)), mask[1:])
            yield from gen_addresses(address & ~(1 << (len(mask) - 1)), mask[1:])

    for action in data:
        if action[0] == 'mask':
            mask = action[1]
        elif action[0] == 'mem':
            address, value = action[1:]
            for address in gen_addresses(address, mask):
                memory[address] = value
        else:
            raise RuntimeError("Unknown action")

    return sum(memory.values())


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
