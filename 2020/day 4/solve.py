import re


def part_1(passports):
    needed_keys = {'byr',
                   'iyr',
                   'eyr',
                   'hgt',
                   'hcl',
                   'ecl',
                   'pid',
                   # 'cid',
                   }
    valid_count = sum(1 for passport in passports if needed_keys <= passport.keys())
    print(valid_count)


def part_2(passports):
    needed_keys = {'byr': lambda s: re.fullmatch(r'\d{4}', s) and (1920 <= int(s) <= 2002),
                   'iyr': lambda s: re.fullmatch(r'\d{4}', s) and (2010 <= int(s) <= 2020),
                   'eyr': lambda s: re.fullmatch(r'\d{4}', s) and (2020 <= int(s) <= 2030),
                   'hgt': lambda s: ((re.fullmatch(r'\d+cm', s) and (150 <= int(s[:-2]) <= 193)) or
                                     (re.fullmatch(r'\d+in', s) and (59 <= int(s[:-2]) <= 76))),
                   'hcl': lambda s: re.fullmatch(r'#[\da-f]{6}', s),
                   'ecl': lambda s: re.fullmatch(r'amb|blu|brn|gry|grn|hzl|oth', s),
                   'pid': lambda s: re.fullmatch(r'\d{9}', s),
                   # 'cid': lambda s: True,
                   }
    valid_count = sum(1 for passport in passports if
                      all(key in passport and needed_keys[key](passport[key]) for key in needed_keys.keys()))
    print(valid_count)


def scan_passports(input_file):
    passports, passport = [], {}

    for line in input_file:
        entries = line.split()
        if len(entries) == 0:
            passports.append(passport)
            passport = {}
            continue

        for entry in entries:
            key, value = entry.split(':')
            passport[key] = value

    passports.append(passport)
    return passports


def main():
    with open('input.txt') as input_file:
        passports = scan_passports(input_file)

    print(passports)
    part_1(passports)
    part_2(passports)


if __name__ == "__main__":
    main()
