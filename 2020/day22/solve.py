from collections import deque

from itertools import islice
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
    def play(deck1, deck2, first_game):
        if max(deck1) > max(deck2) and not first_game:
            return True, None

        seen_decks = set()
        # key = sum(1 << a for a in deck1)
        key = 0
        while len(deck1) > 0 and len(deck2) > 0:
            if key in seen_decks:
                return True, None
            seen_decks.add(key)

            card1 = deck1.popleft()
            card2 = deck2.popleft()

            if len(deck1) >= card1 and len(deck2) >= card2:
                sub_deck1 = deque(islice(deck1, card1), deck1.maxlen)
                sub_deck2 = deque(islice(deck2, card2), deck2.maxlen)
                p1_win, cards = play(sub_deck1, sub_deck2, False)
            else:
                p1_win = card1 > card2

            if p1_win:
                deck1.append(card1)
                deck1.append(card2)
                key += 1 << card2
            else:
                deck2.append(card2)
                deck2.append(card1)
                key -= 1 << card1

        return len(deck1) > 0, deck1 if len(deck1) > 0 else deck2

    game1, deck = play(deque(decks[0]), deque(decks[1]), True)

    return sum((len(deck) - i) * card for i, card in enumerate(deck))


def main():
    decks = get_decks()
    part_1(decks)
    part_2(decks)


if __name__ == "__main__":
    main()
