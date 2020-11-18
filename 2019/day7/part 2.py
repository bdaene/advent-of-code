

from itertools import permutations
from threading import Thread
from queue import SimpleQueue


def solve(input_file, nb_programs=5):
    program = list(map(int, input_file.readline().split(',')))

    best = None
    for phase_settings in permutations(range(5, 10)):
        threads = []
        queues = []
        def launch(program_, thread_id_):

            def input_func():
                # print(f"{threads[thread_id_].name} is waiting input")
                return queues[thread_id_].get()

            def output_func(value):
                # print(f"{threads[thread_id_].name} outputs {value}")
                queues[(thread_id_+1) % nb_programs].put(value)

            execute(program_, input_func=input_func, output_func=output_func)

        for thread_id in range(nb_programs):
            queues.append(SimpleQueue())
            thread = Thread(name=f"program {chr(ord('A')+thread_id)}", target=launch, args=(program[:], thread_id))
            threads.append(thread)
            thread.start()

        for thread_id in range(nb_programs):
            queues[thread_id].put(phase_settings[thread_id])

        queues[0].put(0)

        threads[-1].join()

        result = queues[0].get()
        if best is None or result > best[0]:
            best = (result, phase_settings)

    return best


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
                      99: 0}


def default_input():
    return int(input("Need input: "))


def execute(program, input_func=default_input, output_func=print):

    def get_value(value, flag):
        if flag == 1:
            return value
        return program[value]

    instruction_pointer = 0
    while True:
        flags_, op = divmod(program[instruction_pointer], 100)
        instruction_pointer += 1

        values, flags = [], []
        for i in range(NUMBER_OF_OPERANDS[op]):
            value = program[instruction_pointer]
            values.append(value)
            flags_, flag = divmod(flags_, 10)
            flags.append(flag)
            instruction_pointer += 1

        if op == 1:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = get_value(a, fa) + get_value(b, fb)
        elif op == 2:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = get_value(a, fa) * get_value(b, fb)
        elif op == 3:
            (a,) = values
            program[a] = input_func()
        elif op == 4:
            (a,) = values
            (fa,) = flags
            output_func(get_value(a, fa))
        elif op == 5:
            a, b = values
            fa, fb = flags
            if get_value(a, fa) != 0:
                instruction_pointer = get_value(b, fb)
        elif op == 6:
            a, b = values
            fa, fb = flags
            if get_value(a, fa) == 0:
                instruction_pointer = get_value(b, fb)
        elif op == 7:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = 1 if (get_value(a, fa) < get_value(b, fb)) else 0
        elif op == 8:
            a, b, c = values
            fa, fb, fc = flags
            program[c] = 1 if (get_value(a, fa) == get_value(b, fb)) else 0
        elif op == 99:
            return
        else:
            raise RuntimeError("Something went wrong")


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(*solve(input_file))