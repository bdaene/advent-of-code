from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            ingredients, allergens = line.split(' (contains ')
            ingredients = ingredients.split(' ')
            allergens = allergens[:-2].split(', ')
            data.append((frozenset(ingredients), frozenset(allergens)))
    return data


@timeit
def part_1(data):
    allergen_to_ingredient = {}
    for ingredients, allergens in data:
        for allergen in allergens:
            if allergen not in allergen_to_ingredient:
                allergen_to_ingredient[allergen] = ingredients
            else:
                allergen_to_ingredient[allergen] &= ingredients

    possible_allergens = set()
    for ingredients in allergen_to_ingredient.values():
        possible_allergens |= ingredients

    total = 0
    for ingredients, allergens in data:
        total += len(ingredients - possible_allergens)

    return total


@timeit
def part_2(data):
    allergen_to_ingredients = {}
    for ingredients, allergens in data:
        for allergen in allergens:
            if allergen not in allergen_to_ingredients:
                allergen_to_ingredients[allergen] = ingredients
            else:
                allergen_to_ingredients[allergen] &= ingredients

    allergen_to_ingredients = {key: set(value) for key, value in allergen_to_ingredients.items()}
    allergens = {}

    while len(allergen_to_ingredients) > 0:
        for allergen, ingredients in allergen_to_ingredients.items():
            if len(ingredients) == 1:
                allergen_to_ingredients.pop(allergen)
                ingredient = tuple(ingredients)[0]
                allergens[allergen] = ingredient
                for allergen_, ingredients_ in allergen_to_ingredients.items():
                    ingredients_.discard(ingredient)
                break

    return ','.join(allergens[allergen] for allergen in sorted(allergens))


def main():
    data = get_data()

    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
