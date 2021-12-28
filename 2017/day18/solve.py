from collections import defaultdict
from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            instruction = line.split()
            for i, value in enumerate(instruction):
                try:
                    instruction[i] = int(value)
                except ValueError:
                    continue
            data.append(tuple(instruction))
    return tuple(data)


class Program:
    
    def __init__(self, instructions, default_registers=None):
        self.instruction_pointer = 0
        self.instructions = instructions
        self.registers = defaultdict(int) if default_registers is None else default_registers
        self.snd = None
        self.queue = []
        self.queue_index = 0
        
    def _get_value(self, val):
        if isinstance(val, int):
            return val
        return self.registers[val]

    def run_until_wait(self):
        while 0 <= self.instruction_pointer < len(self.instructions):

            instruction, *values = self.instructions[self.instruction_pointer]

            if instruction == 'snd':
                x = values[0]
                self.snd(self._get_value(x))
            elif instruction == 'set':
                x, y = values
                self.registers[x] = self._get_value(y)
            elif instruction == 'add':
                x, y = values
                self.registers[x] += self._get_value(y)
            elif instruction == 'mul':
                x, y = values
                self.registers[x] *= self._get_value(y)
            elif instruction == 'mod':
                x, y = values
                self.registers[x] %= self._get_value(y)
            elif instruction == 'rcv':
                if self.queue_index >= len(self.queue):
                    return
                x = values[0]
                self.registers[x] = self.queue[self.queue_index]
                self.queue_index += 1
            elif instruction == 'jgz':
                x, y = values
                if self._get_value(x) > 0:
                    self.instruction_pointer += self._get_value(y) - 1
            else:
                raise ValueError(f"Unknown instruction {(instruction, *values)}")

            self.instruction_pointer += 1


@timeit
def part_1(data):

    sounds = []

    def snd(val):
        sounds.append(val)

    program = Program(data)
    program.snd = snd

    program.run_until_wait()
    return sounds[-1]


@timeit
def part_2(data):

    program_0 = Program(data, default_registers={'p': 0})
    program_1 = Program(data, default_registers={'p': 1})

    program_0.snd = lambda val: program_1.queue.append(val)
    program_1.snd = lambda val: program_0.queue.append(val)

    program_0.run_until_wait()
    while program_1.queue_index < len(program_1.queue):
        program_1.run_until_wait()
        program_0.run_until_wait()

    return len(program_0.queue)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
