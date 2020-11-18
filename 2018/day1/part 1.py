

def solve(input_file):
    ans = 0
    for line in input_file:
        ans += int(line)
    return ans


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))