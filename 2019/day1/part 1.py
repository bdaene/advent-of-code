
def solve(input_file):
    ans = 0
    for line in input_file:
        fuel = int(line)//3-2
        ans += fuel
    return ans


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))