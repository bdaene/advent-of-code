

from collections import defaultdict, deque
from decoder import decode


def solve(program):
    view = []

    def output_func(value):
        view.append(chr(value))

    execute(program, output_func=output_func)

    scaffolds_map = ''.join(view)
    print(scaffolds_map)
    scaffolds_map = scaffolds_map.split('\n')

    alignment = 0
    robot_x, robot_y, direction = 0, 0, '^'
    for i, line in enumerate(scaffolds_map):
        for j, cell in enumerate(line):
            if cell == '#' and 0 < i < len(scaffolds_map)-1 and 0 < j < len(scaffolds_map[i])-1 and scaffolds_map[i][j-1] == '#' and scaffolds_map[i][j+1] == '#' and scaffolds_map[i-1][j] == '#' and scaffolds_map[i+1][j] == '#':
                alignment += i*j
            if cell in '^>v<':
                robot_x, robot_y, direction = j, i, cell

    print(robot_x, robot_y, direction)
    directions = deque((('^', 0, -1), ('>', 1, 0), ('v', 0, 1), ('<', -1, 0)))

    path = []
    while directions[0][0] != direction:
        directions.rotate(1)

    def is_scaffold(x, y):
        return 0 <= y < len(scaffolds_map) and 0 <= x < len(scaffolds_map[y]) and scaffolds_map[y][x] == '#'

    while True:
        while is_scaffold(robot_x + directions[0][1], robot_y + directions[0][2]):
            path.append('F')
            robot_x += directions[0][1]
            robot_y += directions[0][2]

        if is_scaffold(robot_x + directions[1][1], robot_y + directions[1][2]):
            directions.rotate(-1)
            path.append('R')
        elif is_scaffold(robot_x + directions[-1][1], robot_y + directions[-1][2]):
            directions.rotate(1)
            path.append('L')
        else:
            break

    path = ''.join(path)
    print(path)

    def deflate(s):
        i = 0
        d = []
        while i < len(s):
            c = 0
            while i + c < len(s) and s[i + c] == 'F':
                c += 1
            if c > 0:
                d.append(c)
                i += c
            if i < len(s):
                d.append(s[i])
                i += 1
        return d

    def get_split(path):
        # Split path in A, B, C
        for a in range(1, len(path)-2):
            A = path[:a]
            for b in range(1, len(path)-1-a):
                B = path[a:a+b]

                Cs = set()
                for subpath in path.split(A):
                    for c in subpath.split(B):
                        if len(c) > 0:
                            Cs.add(c)
                if len(Cs) <= 1:
                    if len(Cs) == 1:
                        C = Cs.pop()
                    else:
                        C = ''
                    A_, B_, C_ = deflate(A), deflate(B), deflate(C)
                    if len(A_) <= 20 and len(B_) <= 20 and len(C_) <= 20:
                        i, main_routine = 0, []
                        while i < len(path):
                            if path.startswith(A, i):
                                main_routine.append('A')
                                i += len(A)
                            elif path.startswith(B, i):
                                main_routine.append('B')
                                i += len(B)
                            elif path.startswith(C, i):
                                main_routine.append('C')
                                i += len(C)
                            else:
                                raise RuntimeError(f'Unknown sequence {path[i:]}')
                        if len(main_routine) <= 20:
                            print(path)
                            print(''.join(A if c == 'A' else B if c == 'B' else C for c in main_routine))
                            return main_routine, A_, B_, C_

    main_routine, A, B, C = get_split(path)
    print(deflate(path))
    print(main_routine)
    print(A)
    print(B)
    print(C)

    program[0] = 2

    def input_func():
        messages = [
            ','.join(main_routine),
            ','.join(map(str, A)),
            ','.join(map(str, B)),
            ','.join(map(str, C)),
            'y']

        for message in messages:
            for c in message:
                print(c, end='')
                yield ord(c)
            print()
            yield ord('\n')

    def output_func2(value):
        if value < 256:
            print(chr(value), end='')
        else:
            print(value)

    execute(program, input_func=input_func().__next__, output_func=output_func2)

    return alignment


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

    decode(program)

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
