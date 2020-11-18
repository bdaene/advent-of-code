

from collections import defaultdict, deque
from threading import Thread, current_thread, Event
from queue import SimpleQueue, Empty
from time import sleep


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


def execute_ascii(int_program, input_func=input, output_func=print):

    def int_input_func():
        while True:
            string = input_func()
            if string[-1] != '\n':
                string += '\n'
            for char in string:
                yield ord(char)

    output = []

    def int_output_func(value):
        if value > 127:
            output_func(value)
        else:
            output.append(value)
            if value == 10:  # '\n1'
                output_func(''.join(chr(char) for char in output))
                output.clear()

    execute(int_program, input_func=int_input_func().__next__, output_func=int_output_func)


def solve(int_program, nb_computers=50):

    threads = []

    programs = [int_program[:] for _ in range(nb_computers)]
    queues = [SimpleQueue() for _ in range(nb_computers)]
    input_buffers = [deque() for _ in range(nb_computers)]
    output_buffers = [deque() for _ in range(nb_computers)]
    msg_counters = [0 for _ in range(nb_computers)]

    idle_nics = [False for _ in range(nb_computers)]

    printer_queue = SimpleQueue()
    nat_queue = SimpleQueue()
    idle_event = Event()

    answer = []

    def launch_printer():

        while True:
            msg = printer_queue.get()
            print(msg)

    printer_thread = Thread(name=f"Printer", target=launch_printer, args=(), daemon=True)
    printer_thread.start()

    def launch_nat():

        last_packet_y = 0

        while True:
            idle_event.wait()
            if all(idle_nic for idle_nic in idle_nics):
                printer_queue.put(f"NAT detected idle network")
                packet = (0, 0)
                assert(not nat_queue.empty())

                while not nat_queue.empty():
                    packet = nat_queue.get()
                    printer_queue.put(f"NAT received {packet}")

                printer_queue.put(f"Sending {packet} to 0")
                if packet[1] == last_packet_y:
                    printer_queue.put(f"NAT : 'Hey I already send {last_packet_y} just before!'")
                    answer.append(last_packet_y)
                    return
                else:
                    last_packet_y = packet[1]
                queues[0].put(packet)
            idle_event.clear()
            sleep(0.1)

    nat_thread = Thread(name=f"NAT", target=launch_nat, args=())
    nat_thread.start()

    def launch(thread_id_):

        def input_function():
            if len(input_buffers[thread_id_]) > 0:
                return input_buffers[thread_id_].popleft()

            try:
                    packet = queues[thread_id_].get(block=False)
                    msg_counters[thread_id_] += 1
                    printer_queue.put(f"{msg_counters[thread_id_]:06d} NIC {thread_id_} received {packet}")
                    input_buffers[thread_id_].extend(packet)
                    return input_buffers[thread_id_].popleft()
            except Empty:
                idle_nics[thread_id_] = True
                idle_event.set()
                return -1

        def output_function(value):
            idle_nics[thread_id_] = False
            output_buffers[thread_id_].append(value)
            if len(output_buffers[thread_id_]) == 3:
                destination = output_buffers[thread_id_].popleft()
                x = output_buffers[thread_id_].popleft()
                y = output_buffers[thread_id_].popleft()
                packet = (x, y)

                msg_counters[thread_id_] += 1
                if destination < nb_computers:
                    printer_queue.put(f"{msg_counters[thread_id_]:06d} NIC {thread_id_} sending {packet} to {destination}")
                    queues[destination].put(packet)
                elif destination == 255:
                    printer_queue.put(f"{msg_counters[thread_id_]:06d} NIC {thread_id_} sending {packet} to NAT")
                    nat_queue.put(packet)
                else:
                    raise RuntimeError(f"{msg_counters[thread_id_]:06d} NIC {thread_id_} failed to send {packet} to {destination}")

        execute(program_=programs[thread_id_], input_func=input_function, output_func=output_function)

    for thread_id in range(nb_computers):
        queues[thread_id].put((thread_id,))
        thread = Thread(name=f"NIC {chr(ord('A')+thread_id)}", target=launch, args=(thread_id,), daemon=True)
        threads.append(thread)

    for thread in threads:
        thread.start()

    nat_thread.join()
    sleep(1)
    return answer


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        int_program_ = list(map(int, input_file.readline().split(',')))
    print(solve(int_program_))
