from collections import deque

from utils import timeit


@timeit
def get_decks():
    with open('input.txt') as input_file:
        assert input_file.readline().strip() == "Player 1:"
        deck1 = []
        for line in input_file:
            if line.isspace():
                break
            deck1.append(int(line))

        assert input_file.readline().strip() == "Player 2:"
        deck2 = []
        for line in input_file:
            if line.isspace():
                break
            deck2.append(int(line))

    return tuple(deck1), tuple(deck2)


@timeit
def part_1(decks):
    deck1, deck2 = decks
    deck1 = deque(deck1)
    deck2 = deque(deck2)

    while len(deck1) > 0 and len(deck2) > 0:
        if deck1[0] > deck2[0]:
            deck1.append(deck1.popleft())
            deck1.append(deck2.popleft())
        else:
            deck2.append(deck2.popleft())
            deck2.append(deck1.popleft())

    deck = deck1 if len(deck1) > 0 else deck2

    return sum((len(deck) - i) * card for i, card in enumerate(deck))


@timeit
def part_2(decks):
    def play(deck1, deck2):

        seen_decks = set()

        while len(deck1) > 0 and len(deck2) > 0:
            key = (deck1, deck2)
            if key in seen_decks:
                return key[0] + key[1], ()
            seen_decks.add(key)

            card1 = deck1[0]
            card2 = deck2[0]
            deck1 = deck1[1:]
            deck2 = deck2[1:]

            if len(deck1) >= card1 and len(deck2) >= card2:
                sub_game = play(deck1[:card1], deck2[:card2])
                if len(sub_game[0]) > 0:
                    deck1 += (card1, card2)
                else:
                    deck2 += (card2, card1)
            else:
                if card1 > card2:
                    deck1 += (card1, card2)
                else:
                    deck2 += (card2, card1)

        return deck1, deck2

    game1 = play(*decks)

    deck = game1[0] if len(game1[0]) > 0 else game1[1]

    return sum((len(deck) - i) * card for i, card in enumerate(deck))


def main():
    decks = get_decks()
    part_1(decks)
    part_2(decks)


if __name__ == "__main__":
    main()
