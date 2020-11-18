

from collections import defaultdict
import keyboard
from lib.pixels import Pixels
from decoder import decode


instruction_pointer = 0
g_program = None

def solve(program):

    program[0] = 2
    x, y = 0, 0
    seq = 0
    ball_x = 0
    pad_x = 0

    screen = Pixels(40, 25, 20, '#000000')
    tiles = {0: '#000000',  # Empty
             1: '#0000ff',  # Wall
             2: '#ffff00',  # Block
             3: '#ffffff',  # Paddle
             4: '#ff0000'}  # Ball

    def input_func():
        screen.display(0.5)
        if keyboard.is_pressed("gauche"): # or ball_x < pad_x:
            return -1
        elif keyboard.is_pressed("droite"): # or ball_x > pad_x:
            return 1
        else:
            return 0

    def output_func(value):
        nonlocal x, y, seq, ball_x, pad_x
        if seq == 0:
            seq = 1
            x = value
        elif seq == 1:
            seq = 2
            y = value
        else:
            seq = 0
            if (x, y) == (-1, 0):
                print(value)
                # decode(g_program, instruction_pointer)
            else:
                screen.put(x, y, tiles[value])
                if value == 3:
                    pad_x = x
                elif value == 4:
                    ball_x = x

    execute(program, input_func=input_func, output_func=output_func)


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
    global instruction_pointer
    global g_program

    program = defaultdict(int)
    for index, value in enumerate(program_):
        program[index] = value

    g_program = program

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
