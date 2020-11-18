
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
OPERATIONS = {1:  'add',
              2:  'multiply',
              3:  'input',
              4:  'output',
              5:  'jmp-true',
              6:  'jmp-zero',
              7:  'less than',
              8:  'equals',
              9:  'chg base',
              99: 'halt'}

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

FLAGS = {0: 'A',  # Absolute position in memory
         1: 'V',  # Direct value
         2: 'R',  # Position relative to the relative base
         }


def decode(program, current_instruction=None, relative_base=None):
    instruction_pointer = 0
    length = max(program) if isinstance(program, dict) else len(program)

    while instruction_pointer < length:
        instruction = f"{'>' if instruction_pointer == current_instruction else '@' if instruction_pointer == relative_base else ' '}{instruction_pointer: 10} "
        flags_, op = divmod(program[instruction_pointer], 100)
        instruction_pointer += 1

        if op not in OPERATIONS or flags_ < 0 or any(flag not in FLAGS for flag in map(int, str(flags_))):
            print(instruction + f"{flags_ * 100 + op: 10}")
            continue

        values, flags = [], []
        for i in range(NUMBER_OF_OPERANDS[op]):
            values.append(program[instruction_pointer])
            flags_, flag = divmod(flags_, 10)
            flags.append(flag)
            instruction_pointer += 1

        instruction += f"{OPERATIONS[op]: >10} "
        instruction += ' '.join(f"{value: 9}{FLAGS[flag]}" for value, flag in zip(values, flags))

        print(instruction)
    print()


if __name__ == "__main__":
    file_path = input("Program to decode: ")
    with open(file_path, 'r') as input_file:
        program = tuple(map(int, input_file.readline().strip().split(',')))
    decode(program)
