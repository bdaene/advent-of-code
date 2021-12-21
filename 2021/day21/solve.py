import re
from utils import timeit
from itertools import islice, cycle, product
from collections import Counter


@timeit
def get_data():
    pattern = re.compile(r'Player (\d+) starting position: (\d+)')
    with open('input.txt') as input_file:
        return {
            int(player): int(position)
            for player, position in [pattern.match(line).groups() for line in input_file]
        }


def deterministic_dice():
    value = 1
    while True:
        yield value
        value += 1
        value = (value - 1) % 100 + 1


@timeit
def part_1(data, track_length=10):
    players = data.copy()
    dice = deterministic_dice()
    scores = {player: 0 for player in players}
    rolls = 0
    for player in cycle(players):
        total = sum(islice(dice, 3))
        rolls += 3
        players[player] = (players[player] + total - 1) % track_length + 1
        scores[player] += players[player]
        if scores[player] >= 1000:
            return min(scores.values()) * rolls


@timeit
def part_2(data):
    dice_distribution = Counter()
    for dices in product((1, 2, 3), repeat=3):
        dice_distribution[sum(dices)] += 1

    positions = (data[1]-1, data[2]-1)
    scores = (0, 0)
    player = 0
    start_state = (positions, scores)

    states = {start_state: 1}
    wins = [0, 0]

    while states:
        new_states = Counter()
        for ((position_0, position_1), (score_0, score_1)), count in states.items():
            for dice, factor in dice_distribution.items():
                new_position = (position_0 + dice) % 10
                new_score = score_0 + new_position + 1
                if new_score >= 21:
                    wins[player] += factor * count
                else:
                    new_state = ((position_1, new_position), (score_1, new_score))
                    new_states[new_state] += factor * count

        player = 1-player
        states = new_states

    print(wins)
    return max(wins)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
