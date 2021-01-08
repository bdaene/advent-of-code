from heapq import heappush, heappop

from utils import timeit


@timeit
def get_boss():
    boss = {}
    with open('input.txt') as input_file:
        for line in input_file:
            stat, value = line.split(': ')
            boss[stat] = int(value)

    return boss


cost = {'Magic Missile': 53,
        'Drain': 73,
        'Shield': 113,
        'Poison': 173,
        'Recharge': 229,
        'Boss': 0,
        }


def get_next_state(state, spell, boss_damage, hard_mode):
    used_mana, boss_hit_points, hit_points, mana, effects, player_turn = state

    if hard_mode and player_turn:
        hit_points -= 1
        if hit_points <= 0:
            return used_mana, boss_hit_points, hit_points, mana, effects, not player_turn

    mana -= cost[spell]
    if mana < 0:
        return None

    effects_ = {}
    armor = 0
    for name, turns in effects.items():
        if name == 'Shield':
            armor += 7
        elif name == 'Poison':
            boss_hit_points -= 3
        elif name == 'Recharge':
            mana += 101
        else:
            raise ValueError(f"Unknown effect : {name}")
        if turns > 1:
            effects_[name] = turns - 1
    effects = effects_

    if spell in effects:
        return None

    if boss_hit_points <= 0:
        return used_mana, boss_hit_points, hit_points, mana, effects_, player_turn

    used_mana += cost[spell]
    if spell == 'Magic Missile':
        boss_hit_points -= 4
    elif spell == 'Drain':
        boss_hit_points -= 2
        hit_points += 2
    elif spell == 'Shield':
        effects['Shield'] = 6
    elif spell == 'Poison':
        effects['Poison'] = 6
    elif spell == 'Recharge':
        effects['Recharge'] = 5
    elif spell == 'Boss':
        hit_points -= max(1, boss_damage - armor)
    else:
        raise ValueError(f"Unknown spell : {spell}")

    return used_mana, boss_hit_points, hit_points, mana, effects, not player_turn


@timeit
def part_1(boss, hit_points=50, mana=500, hard_mode=False):
    boss_damage = boss['Damage']

    heap = [(0, boss['Hit Points'], hit_points, mana, {}, True)]
    while len(heap) > 0:
        state = heappop(heap)
        used_mana, boss_hit_points, hit_points, mana, effects, player_turn = state
        if boss_hit_points <= 0:
            return state[0]
        if hit_points <= 0:
            continue

        if player_turn:
            if hard_mode:
                hit_points -= 1
                if hit_points <= 0:
                    continue

            for spell in {'Magic Missile', 'Drain', 'Shield', 'Poison', 'Recharge'}:
                next_state = get_next_state(state, spell, boss_damage, hard_mode)
                if next_state is not None:
                    heappush(heap, next_state)
        else:
            next_state = get_next_state(state, 'Boss', boss_damage, hard_mode)
            if next_state is not None:
                heappush(heap, next_state)


@timeit
def part_2(boss):
    return part_1.func(boss, hard_mode=True)


def main():
    boss = get_boss()
    part_1(boss)
    part_2(boss)


if __name__ == "__main__":
    main()
