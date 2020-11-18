

def solve(input_file):
    fabric = [[0 for col in range(1000)] for row in range(1000)]
    claims = input_file.read().splitlines()
    for claim in claims:
        claim_id, at, pos, size = claim.split(' ')
        x, y = map(int, pos[:-1].split(','))
        sx, sy = map(int, size.split('x'))

        for row in range(y, y+sy):
            for col in range(x, x+sx):
                fabric[row][col] += 1

    for claim in claims:
        claim_id, at, pos, size = claim.split(' ')
        x, y = map(int, pos[:-1].split(','))
        sx, sy = map(int, size.split('x'))

        if all(fabric[row][col] == 1 for row in range(y, y+sy) for col in range(x, x+sx)):
            return claim_id


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        print(solve(input_file))