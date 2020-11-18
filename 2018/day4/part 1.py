
from collections import Counter


def solve(input_file):
    records = input_file.read().splitlines()
    records.sort()

    sleeps = []
    guard, start = None, None
    for record in records:
        date, time, event, data = record.split(' ')[:4]
        if event == "Guard":
            guard = int(data[1:])
            time = None
            continue
        hour, minute = map(int, time[:-1].split(':'))
        if event == "falls":
            start = minute
        else:
            end = minute
            sleeps.append((guard, start, end))

    count = Counter()
    for sleep in sleeps:
        guard, start, end = sleep
        for minute in range(start, end):
            count[(guard, minute)] += 1

    best = max(count, key=count.get)

    return best[0] * best[1]


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
