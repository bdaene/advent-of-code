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

    print(len(memory))
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

    print(len(memory))
    return sum(memory.values())


def apply_mask(address, mask):
    address_ = []
    for m in reversed(mask):
        address, bit = divmod(address, 2)
        if m == '0':
            address_.append('0' if bit == 0 else '1')
        else:
            address_.append(m)
    return ''.join(address_)


@timeit
def part_2_bis(data, size=36):
    memory = {}

    mask = '0' * size

    for action in data:
        if action[0] == 'mask':
            mask = action[1]
            continue

        address, value = action[1:]
        address = apply_mask(address, mask)

        for add in tuple(memory):
            if any(a != b and a != 'X' and b != 'X' for a, b in zip(add, address)):
                continue  # No conflict

            val = memory.pop(add)
            for i, b in enumerate(address):
                if add[i] == b or b == 'X':
                    continue
                add_0 = add[:i] + address[i] + add[i + 1:]
                add_1 = add[:i] + ('1' if address[i] == '0' else '0') + add[i + 1:]

                memory[add_1] = val
                add = add_0

        memory[address] = value

    print(len(memory))
    return sum(value * 2 ** (address.count('X')) for address, value in memory.items())


@timeit
def part_2_ter(data, size=36):
    memory = {}
    mask = '0' * size

    used_addresses = {}

    def add_address(address):
        node = used_addresses
        for a in address:
            if a not in node:
                node[a] = {}
            node = node[a]
        node[address] = '$'

    def get_addresses(address):
        stack = [used_addresses]
        for a in address:
            stack_ = []
            for node in stack:
                if a == 'X':
                    stack_.extend(node.values())
                else:
                    if a in node:
                        stack_.append(node[a])
                    if 'X' in node:
                        stack_.append(node['X'])
            stack = stack_
        addresses = []
        for node in stack:
            addresses.extend(node)
        return addresses

    for action in data:
        if action[0] == 'mask':
            mask = action[1]
            continue

        address, value = action[1:]
        address = apply_mask(address, mask)

        for add in get_addresses(address):
            if add not in memory:
                continue
            val = memory.pop(add)
            for i, b in enumerate(address):
                if add[i] == b or b == 'X':
                    continue
                add_0 = add[:i] + address[i] + add[i + 1:]
                add_1 = add[:i] + ('1' if address[i] == '0' else '0') + add[i + 1:]

                memory[add_1] = val
                add_address(add_1)
                add = add_0

        memory[address] = value
        add_address(address)

    print(len(memory))
    return sum(value * 2 ** (address.count('X')) for address, value in memory.items())


def main():
    data = get_data()
    part_1(data)
    part_2(data)
    part_2_bis(data)
    part_2_ter(data)


if __name__ == "__main__":
    main()
