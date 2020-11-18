
import re

PATTERN = re.compile(r'(\d*) players; last marble is worth (\d*) points')


def solve(input_file):
    for line in input_file:
        nb_players, last_marble = map(int, PATTERN.match(line).groups())
        high_score = max(play(nb_players, last_marble))
        print(f"{nb_players} players; last marble is worth {last_marble} points: high score is {high_score}")


def play(nb_players, last_marble):

    class Marble:
        def __init__(self, value, left, right):
            self.value = value
            self.left = left
            self.right = right

        def __repr__(self):
            s = [f"({self.value:2})"]
            marble = self.right
            while marble is not self:
                s.append(f"{marble.value:2}")
                marble = marble.right
            return ' '.join(s)

    current_marble = Marble(0, None, None)
    current_marble.left = current_marble
    current_marble.right = current_marble
    nb_marble = 1

    players_score = [0] * nb_players
    current_player = 0
    while nb_marble <= last_marble:
        if nb_marble % 23 == 0:
            removed_marble = current_marble.left.left.left.left.left.left.left
            score = nb_marble + removed_marble.value
            removed_marble.left.right = removed_marble.right
            removed_marble.right.left = removed_marble.left
            current_marble = removed_marble.right
            nb_marble += 1
            players_score[current_player] += score
        else:
            new_marble = Marble(nb_marble, current_marble.right, current_marble.right.right)
            new_marble.left.right = new_marble
            new_marble.right.left = new_marble
            current_marble = new_marble
            nb_marble += 1
        current_player = (current_player + 1) % nb_players

    return players_score


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        solve(input_file)
