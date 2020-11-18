

def solve(match=505961):
    match = tuple(map(int, str(match)))
    recipes = [3, 7]
    elves = [0, 1]
    searched = 0

    def search():
        nonlocal searched
        while searched + len(match) <= len(recipes):
            if all(recipes[searched + k] == m for k, m in enumerate(match)):
                return searched
            searched += 1
        return None

    while search() is None:
        score = sum(recipes[elf] for elf in elves)
        recipes.extend(map(int, str(score)))
        elves = list((elf + recipes[elf] + 1) % len(recipes) for elf in elves)

    return search()


if __name__ == "__main__":
    print(solve())
