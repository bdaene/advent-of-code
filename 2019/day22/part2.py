
from lib.euclide import invMod


def solve(instructions, nb_cards, nb_shuffles, end_position):

    a, b = 1, 0
    for instruction in instructions:
        if instruction == "deal into new stack":
            # ap+b -> -(ap+b) - 1 = -ap -b -1
            a, b = -a, -b-1
        elif instruction.startswith("cut"):
            n = int(instruction[4:])
            # ap+b -> (ap +b) - n1 = ap + b-n1
            b -= n
        elif instruction.startswith("deal with increment"):
            n = int(instruction[20:])
            # ap+b -> (ap+b)*n1 = anp + bn
            a, b = a*n, b*n
        else:
            raise RuntimeError(f"Unknown instruction : '{instruction}'")

    a %= nb_cards
    b %= nb_cards

    print(f"One complete shuffle moves card at position p to position ({a}*p+{b})%{nb_cards}")
    print(f"For example, card {end_position} moves to {(a*end_position+b)%nb_cards}")

    a_n = pow(a, nb_shuffles, nb_cards)
    b_n = b * (a_n - 1) * invMod(a - 1, nb_cards) % nb_cards

    print(f"After {nb_shuffles} shuffles, card {end_position} moves to {(a_n*end_position + b_n) % nb_cards}")

    start_position = (end_position - b_n) * invMod(a_n, nb_cards) % nb_cards
    print(f"After {nb_shuffles} shuffles, card {start_position} moves to {(a_n * start_position + b_n) % nb_cards}")


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        instructions_ = list(line[:-1] for line in input_file)
    solve(instructions_, 10007, 1, 2019)
    solve(instructions_, 119315717514047, 101741582076661, 2020)
