

def solve(input_file):
    seen = set()
    sequence = []
    for line in input_file:
        sequence.append(int(line))

    ans, i = 0, 0
    while ans not in seen:
        seen.add(ans)
        ans += sequence[i]
        i = (i+1) % len(sequence)

    return ans


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))
