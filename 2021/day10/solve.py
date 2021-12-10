from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        return [line.strip() for line in input_file]


BRACKETS = {opening: closing for opening, closing in zip('([{<', ')]}>')}


@timeit
def part_1(data):
    brackets_score = {closing: score for closing, score in zip(')]}>', (3, 57, 1197, 25137))}
    score = 0
    for line in data:
        stack = []
        for c in line:
            if c in BRACKETS:
                stack.append(c)
            else:
                if not stack or BRACKETS[stack.pop()] != c:
                    score += brackets_score[c]
                    break

    return score


@timeit
def part_2(data):
    brackets_score = {closing: score for closing, score in zip(')]}>', (1, 2, 3, 4))}
    scores = []
    for line in data:
        stack = []
        corrupted = False
        for c in line:
            if c in BRACKETS:
                stack.append(c)
            else:
                if not stack or BRACKETS[stack.pop()] != c:
                    corrupted = True
                    break

        if not corrupted:
            score = 0
            for c in reversed(stack):
                score *= 5
                score += brackets_score[BRACKETS[c]]
            scores.append(score)

    return sorted(scores)[len(scores)//2]


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
