

from collections import defaultdict, deque


def solve(program):

    directions = {
        (0, 1):  1,
        (0, -1): 2,
        (-1, 0): 3,
        (1, 0):  4}

    tiles = {0: '#',  # Wall
             1: '.',  # Empty space
             2: 'O'}  # Oxygen system

    explored_space = {(0, 0): (0, '.', None)}
    droid_x, droid_y = 0, 0
    path_to_travel = []
    to_explore = deque((direction, 1, (0, 0)) for direction in directions)
    oxygen = None

    def input_func():
        if len(path_to_travel) == 0:
            while len(to_explore) > 0 and to_explore[0][0] in explored_space:
                to_explore.popleft()
            if len(to_explore) == 0:
                show_explored_space()
                return 0
            path_backward = [to_explore[0][0]]
            path_forward = []
            target = to_explore[0][2]
            droid = droid_x, droid_y
            while explored_space[target][2] != explored_space[droid][2]:
                if explored_space[target][0] > explored_space[droid][0]:
                    path_backward.append(target)
                    target = explored_space[target][2]
                else:
                    path_forward.append(droid)
                    droid = explored_space[droid][2]
            if droid == target:
                path_to_travel.extend(path_backward + [target] + path_forward[::-1])
            else:
                path_to_travel.extend(path_backward + [target, explored_space[target][2], droid] + path_forward[::-1])
            path_to_travel.pop()

        x, y = path_to_travel[-1]
        print(f"Moving droid to {x, y}")
        return directions[(x - droid_x, y - droid_y)]

    def output_func(value):
        nonlocal droid_x, droid_y, oxygen
        x, y = path_to_travel.pop()
        if (x, y) not in explored_space:
            assert((x, y)  == to_explore[0][0])
            target, distance, parent = to_explore[0]
            explored_space[target] = (distance, tiles[value], parent)
        distance = explored_space[(x, y)][0]

        if value in (1, 2):
            droid_x, droid_y = x, y
            for dx, dy in directions:
                to_explore.append(((droid_x + dx, droid_y + dy), distance + 1, (droid_x, droid_y)))
            if value == 2:
                oxygen = (x, y)
                show_explored_space()
                print(f"Oxygen system found at {oxygen}. Distance {explored_space[oxygen][0]}")

    def show_explored_space():
        min_x = min(x for x, y in explored_space)
        max_x = max(x for x, y in explored_space)
        min_y = min(y for x, y in explored_space)
        max_y = max(y for x, y in explored_space)

        s = '\n'.join(''.join('D' if (x, y) == (droid_x, droid_y)
                              else explored_space[(x, y)][1] if (x, y) in explored_space
                              else ' '
                              for x in range(min_x, max_x + 1))
                      for y in reversed(range(min_y, max_y + 1)))
        print(s)
        print()

    show_explored_space()
    execute(program, input_func=input_func, output_func=output_func)

    filled = set()
    to_fill = [oxygen]
    time = 0
    while len(to_fill) > 0:
        time += 1
        to_fill_ = []
        for position in to_fill:
            if position in filled:
                continue
            filled.add(position)
            x, y = position
            for dx, dy in directions:
                target = (x + dx, y + dy)
                if target not in filled and explored_space[target][1] == '.':
                    to_fill_.append(target)
        to_fill = to_fill_

    return time - 1


"""
Operations :
    1 a b c     add             a + b -> c
    2 a b c     multiply        a * b -> c
    3 a         input           input -> a
    4 a         output          a -> output
    5 a b       jump-if-true    (a != 0) => b -> instruction pointer
    6 a b       jump-if-false   (a == 0) => b -> instruction pointer
    7 a b c     less than       (a < b) -> c
    8 a b c     equals          (a == b) -> c
    9 a         change base     relative_base += a
   99           halt
"""
NUMBER_OF_OPERANDS = {1: 3,
                      2: 3,
                      3: 1,
                      4: 1,
                      5: 2,
                      6: 2,
                      7: 3,
                      8: 3,
                      9: 1,
                      99: 0}


def default_input():
    return int(input("Need input: "))


def execute(program_, input_func=default_input, output_func=print):

    program = defaultdict(int)
    for index, value in enumerate(program_):
        program[index] = value

    relative_base = 0

    def get_value(flag_, index_):
        if flag_ == 0:
            return program[index_]
        elif flag_ == 1:
            return index_
        elif flag_ == 2:
            return program[relative_base + index_]
        else:
            raise RuntimeError(f"Unknown flag {flag_} in get_value({flag_}, {index_})")

    def set_value(flag_, index_, value_):
        if flag_ == 0:
            program[index_] = value_
        elif flag_ == 1:
            raise RuntimeError(f"Cannot set to value in set_value({flag_}, {index_}, {value_})")
        elif flag_ == 2:
            program[relative_base + index_] = value_
        else:
            raise RuntimeError(f"Unknown flag {flag_} in set_value({flag_}, {index_}, {value_})")

    instruction_pointer = 0
    while True:
        flags_, op = divmod(program[instruction_pointer], 100)
        instruction_pointer += 1

        values, flags = [], []
        for i in range(NUMBER_OF_OPERANDS[op]):
            values.append(program[instruction_pointer])
            flags_, flag = divmod(flags_, 10)
            flags.append(flag)
            instruction_pointer += 1

        if op == 1:
            a, b, c = values
            fa, fb, fc = flags
            set_value(fc, c, get_value(fa, a) + get_value(fb, b))
        elif op == 2:
            a, b, c = values
            fa, fb, fc = flags
            set_value(fc, c, get_value(fa, a) * get_value(fb, b))
        elif op == 3:
            (a,) = values
            (fa,) = flags
            set_value(fa, a, input_func())
        elif op == 4:
            (a,) = values
            (fa,) = flags
            output_func(get_value(fa, a))
        elif op == 5:
            a, b = values
            fa, fb = flags
            if get_value(fa, a) != 0:
                instruction_pointer = get_value(fb, b)
        elif op == 6:
            a, b = values
            fa, fb = flags
            if get_value(fa, a) == 0:
                instruction_pointer = get_value(fb, b)
        elif op == 7:
            a, b, c = values
            fa, fb, fc = flags
            set_value(fc, c, 1 if (get_value(fa, a) < get_value(fb, b)) else 0)
        elif op == 8:
            a, b, c = values
            fa, fb, fc = flags
            set_value(fc, c, 1 if (get_value(fa, a) == get_value(fb, b)) else 0)
        elif op == 9:
            (a,) = values
            (fa,) = flags
            relative_base += get_value(fa, a)
        elif op == 99:
            return
        else:
            raise RuntimeError("Something went wrong")


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        program = list(map(int, input_file.readline().split(',')))
    print(solve(program))
