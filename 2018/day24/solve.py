import re
from utils import timeit


class Group:

    _pattern = re.compile(r'(\d+) units each with (\d+) hit points (?:\((.*)\) )?'
                          r'with an attack that does (\d+) (\w+) damage at initiative (\d+)')

    def __init__(self, units, hit_points, weaknesses, immunities, attack, attack_type, initiative):
        self.units = units
        self.hit_points = hit_points
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative

        self.army = None
        self.army_id = 0

    @staticmethod
    def from_string(string):
        units, hit_points, traits, attack, attack_type, initiative = Group._pattern.match(string).groups()
        weaknesses, immunities = set(), set()
        if traits is not None:
            for trait in traits.split('; '):
                if trait.startswith('weak to '):
                    weaknesses |= set(trait[8:].split(', '))
                elif trait.startswith('immune to '):
                    immunities |= set(trait[10:].split(', '))
        return Group(int(units), int(hit_points), weaknesses, immunities, int(attack), attack_type, int(initiative))

    def __str__(self):
        return f"{self.army} group {self.army_id}"

    @property
    def effective_power(self):
        return self.units * self.attack

    def damage_to(self, other):
        if self.attack_type in other.immunities:
            return 0
        elif self.attack_type in other.weaknesses:
            return self.effective_power * 2
        else:
            return self.effective_power

    def __hash__(self):
        return hash((self.army, self.army_id))


@timeit
def get_data():
    data = {}
    with open('input.txt') as input_file:
        force = None
        count = 0
        for line in input_file:
            if force is None:
                force = line[:-2]
                data[force] = []
                count = 0
            elif line.isspace():
                force = None
            else:
                count += 1
                group = Group.from_string(line)
                group.army = force
                group.army_id = count
                data[force].append(group)

    return data


def fight(armies):
    while all(len(armies[army]) > 0 for army in armies):
        # for army in armies:
        #     print(f"{army}:")
        #     for i, group in enumerate(armies[army], 1):
        #         print(f"Group {group.army_id} contains {group.units} units")
        # print()

        # Target selection
        targets = {}

        for army, groups in armies.items():
            defending_groups = list(group_ for army_, groups_ in armies.items() for group_ in groups_ if army_ != army)
            for group in sorted(groups, reverse=True, key=lambda g: (g.effective_power, g.initiative)):
                group_targets = list(group_ for group_ in defending_groups if group.damage_to(group_) > 0
                                     and group_ not in targets.values())
                # for target in group_targets:
                #     print(f"{group} would deal defending group {target.army_id} {group.damage_to(target)} damage")
                group_targets.sort(reverse=True, key=lambda g: (group.damage_to(g), g.effective_power, g.initiative))
                if group_targets:
                    targets[group] = group_targets[0]
        # print()

        # Attacking
        total_kills = 0
        groups = list(group_ for groups_ in armies.values() for group_ in groups_)
        groups.sort(reverse=True, key=lambda g: g.initiative)
        for group in groups:
            if group.units <= 0 or group not in targets:
                continue

            target = targets[group]
            kills = min(group.damage_to(target) // target.hit_points, target.units)
            # print(f"{group} attacks defending group {target.army_id}, killing {kills} units")
            total_kills += kills

            target.units -= kills
            if target.units <= 0:
                armies[target.army].remove(target)

        # print()
        if total_kills <= 0:
            break

    # for army in armies:
    #     print(f"{army}:")
    #     for i, group in enumerate(armies[army], 1):
    #         print(f"Group {group.army_id} contains {group.units} units")
    # print()

    return armies


@timeit
def part_1():
    armies = fight(get_data())
    return sum(sum(group.units for group in groups) for groups in armies.values())


@timeit
def part_2():

    def immune_win(boost):
        armies = get_data.func()
        for group in armies['Immune System']:
            group.attack += boost
        armies = fight(armies)
        return len(armies['Infection']) == 0 and armies

    b = 1
    while not immune_win(b):
        b *= 2

    min_b = b // 2
    max_b = b
    while min_b + 1 < max_b:
        mid_b = (min_b + max_b) // 2
        if immune_win(mid_b):
            max_b = mid_b
        else:
            min_b = mid_b

    return sum(sum(group.units for group in groups) for groups in immune_win(max_b).values())


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
