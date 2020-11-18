

def solve(instructions, nb_cards_, cards_to_follow):
    print('\n'.join(instructions))

    def deal_into_new_stack(cards):
        """ Reverse the order of the cards """
        return {card: nb_cards_-1-position for card, position in cards.items()}

    def cut(cards, n):
        """ Cut n1 tops card and put it at the bottom """
        n %= nb_cards_
        return {card: (position - n if position >= n else nb_cards_ - n + position) for card, position in cards.items()}

    def deal_with_increment(cards, n):
        return {card: (position * n) % nb_cards_ for card, position in cards.items()}

    #  number: position
    cards = {card: card for card in cards_to_follow}

    for instruction in instructions:
        if instruction == "deal into new stack":
            cards = deal_into_new_stack(cards)
        elif instruction.startswith("cut"):
            cards = cut(cards, int(instruction[4:]))
        elif instruction.startswith("deal with increment"):
            cards = deal_with_increment(cards, int(instruction[20:]))
        else:
            raise RuntimeError(f"Unknown instruction : '{instruction}'")

    print(cards)


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        instructions_ = list(line[:-1] for line in input_file)
    solve(instructions_, 10007, (2019,))
