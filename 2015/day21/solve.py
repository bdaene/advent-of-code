from utils import timeit


@timeit
def get_data():
    boss = {}
    with open('input.txt') as input_file:
        for line in input_file:
            stat, value = line.split(': ')
            boss[stat] = int(value)

    with open('shop.txt') as input_file:
        weapons = {}
        assert input_file.readline().startswith('Weapons')
        for line in input_file:
            if line.isspace():
                break
            name, cost, damage, armor = line.split()
            weapons[name] = {'cost': int(cost), 'damage': int(damage), 'armor': int(armor)}

        armors = {}
        assert input_file.readline().startswith('Armor')
        for line in input_file:
            if line.isspace():
                break
            name, cost, damage, armor = line.split()
            armors[name] = {'cost': int(cost), 'damage': int(damage), 'armor': int(armor)}

        rings = {}
        assert input_file.readline().startswith('Rings')
        for line in input_file:
            if line.isspace():
                break
            name, name_, cost, damage, armor = line.split()
            rings[name + ' ' + name_] = {'cost': int(cost), 'damage': int(damage), 'armor': int(armor)}

    shop = {'weapons': weapons, 'armors': armors, 'rings': rings}
    return boss, shop


@timeit
def part_1(data, hit_points=100):
    boss, shop = data

    def win(weapon, armor, ring_a, ring_b):
        damage = sum(o['damage'] for o in (weapon, armor, ring_a, ring_b))
        armor = sum(o['armor'] for o in (weapon, armor, ring_a, ring_b))

        attack = max(1, damage - boss['Armor'])
        boss_attack = max(1, boss['Damage'] - armor)

        return hit_points / boss_attack >= boss['Hit Points'] / attack

    none_object = {'cost': 0, 'damage': 0, 'armor': 0}
    weapons = tuple(shop['weapons'].values())
    armors = tuple(shop['armors'].values())
    rings = tuple(shop['rings'].values())

    best = 9999999999
    for weapon in weapons:
        for armor in armors + (none_object,):
            for i, ring_a in enumerate(rings + (none_object,), 1):
                for ring_b in rings[i:] + (none_object,):
                    if win(weapon, armor, ring_a, ring_b):
                        best = min(best, sum(o['cost'] for o in (weapon, armor, ring_a, ring_b)))

    return best


@timeit
def part_2(data, hit_points=100):
    boss, shop = data

    def win(weapon, armor, ring_a, ring_b):
        damage = sum(o['damage'] for o in (weapon, armor, ring_a, ring_b))
        armor = sum(o['armor'] for o in (weapon, armor, ring_a, ring_b))

        attack = max(1, damage - boss['Armor'])
        boss_attack = max(1, boss['Damage'] - armor)

        return hit_points / boss_attack >= boss['Hit Points'] / attack

    none_object = {'cost': 0, 'damage': 0, 'armor': 0}
    weapons = tuple(shop['weapons'].values())
    armors = tuple(shop['armors'].values())
    rings = tuple(shop['rings'].values())

    best = 0
    for weapon in weapons:
        for armor in armors + (none_object,):
            for i, ring_a in enumerate(rings + (none_object,), 1):
                for ring_b in rings[i:] + (none_object,):
                    if not win(weapon, armor, ring_a, ring_b):
                        best = max(best, sum(o['cost'] for o in (weapon, armor, ring_a, ring_b)))

    return best


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
