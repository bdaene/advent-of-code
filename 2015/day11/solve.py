from utils import timeit

alphabet = 'abcdefghijklmnopqrstuvwxyz'
next_letter = {a: b for a, b in zip(alphabet, 'bcdefghjjkmmnppqrstuvwxyz')}


def get_next(password):
    i = -1
    while i > -len(password) and password[i] == 'z':
        i -= 1
    if i == - len(password):
        return 'a' * (len(password) + 1)
    return password[:i] + next_letter[password[i]] + 'a' * (-i - 1)


@timeit
def part_1(password='hepxcrrq'):
    password = get_next(password)
    three_letters = [alphabet[i:i + 3] for i in range(len(alphabet) - 2)]
    two_letters = [c + c for c in alphabet]
    while not (
            any(w in password for w in three_letters) and sum(1 for w in two_letters if w in password) >= 2):
        password = get_next(password)

    return password


@timeit
def part_2():
    return part_1.func(part_1.func())


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
