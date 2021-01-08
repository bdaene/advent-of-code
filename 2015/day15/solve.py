from utils import timeit


@timeit
def get_ingredients():
    ingredients = {}
    with open('input.txt') as input_file:
        for line in input_file:
            ingredient, values = line.split(': ')
            values = [prop.split(' ') for prop in values.split(', ')]
            ingredients[ingredient] = {name: int(value) for name, value in values}
    return ingredients


@timeit
def part_1(ingredients):
    ingredient_list = tuple(ingredients)
    value_names = tuple(ingredients[ingredient_list[0]].keys() - {'calories'})

    def get_best(i, s, values):
        if i == 0:
            total = 1
            for name in value_names:
                total *= max(0, values[name])
            return total

        best = 0
        for q in range(s + 1):
            best = max(best, get_best(i - 1, s - q,
                                      {name: values[name] + q * ingredients[ingredient_list[i - 1]][name] for
                                       name in value_names}))

        return best

    return get_best(len(ingredients), 100, {name: 0 for name in value_names})


@timeit
def part_2(ingredients):
    ingredient_list = tuple(ingredients)
    value_names = frozenset(ingredients[ingredient_list[0]]) - {'calories'}

    def get_best(i, s, c, values):
        if c < 0:
            return 0

        if i == 0:
            if c != 0:
                return 0

            total = 1
            for name in value_names:
                total *= max(0, values[name])
            return total

        best = 0
        ingredient_values = ingredients[ingredient_list[i - 1]]
        for q in range(s + 1):
            best = max(best, get_best(i - 1, s - q, c - q * ingredient_values['calories'],
                                      {name: values[name] + q * ingredient_values[name] for name in
                                       value_names}))

        return best

    return get_best(len(ingredients), 100, 500, {name: 0 for name in value_names})


def main():
    ingredients = get_ingredients()
    # part_1(ingredients)
    part_2(ingredients)


if __name__ == "__main__":
    main()
