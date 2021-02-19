from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for move in input_file.readline().strip().split(','):
            if move[0] == 's':
                data.append(('s', int(move[1:])))
            elif move[0] == 'x':
                a, b = move[1:].split('/')
                data.append(('x', int(a), int(b)))
            elif move[0] == 'p':
                a, b = move[1:].split('/')
                data.append(('p', a, b))
        return tuple(data)


def dance(programs, actions):
    for action, *values in actions:
        if action == 's':
            x = values[0]
            programs = programs[-x:] + programs[:-x]
        elif action == 'x':
            a, b = values
            programs[a], programs[b] = programs[b], programs[a]
        elif action == 'p':
            a, b = values
            a, b = programs.index(a), programs.index(b)
            programs[a], programs[b] = programs[b], programs[a]
    return programs


@timeit
def part_1(data, nb_programs=16):
    programs = [chr(ord('a') + i) for i in range(nb_programs)]
    programs = dance(programs, data)
    return ''.join(programs)


@timeit
def part_2(data, nb_programs=16, nb_dances=1000000000):

    programs = [chr(ord('a') + i) for i in range(nb_programs)]
    i, seen = 0, {tuple(programs): 0}
    while i != nb_dances:
        i += 1
        programs = dance(programs, data)
        key = tuple(programs)
        if key in seen:
            repeat_time = i - seen[key]
            nb_dances -= (nb_dances-i)//repeat_time*repeat_time
        seen[key] = i

    return ''.join(programs)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
