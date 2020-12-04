#!/usr/bin/python3
from dataclasses import dataclass
import re


@dataclass
class Passport:
    byr:str = ''
    iyr:str = ''
    eyr:str = ''
    hgt:str = ''
    hcl:str = ''
    ecl:str = ''
    pid:str = ''
    cid:str = ''

    _validations = {
        'byr': bool,
        'iyr': bool,
        'eyr': bool,
        'hgt': bool,
        'hcl': bool,
        'ecl': bool,
        'pid': bool,
    }

    @classmethod
    def from_batch(cls, desc):
        kwargs = dict(w.split(':') for w in desc.split())
        return cls(**kwargs)

    @property
    def is_valid(self):
        return all(validation(getattr(self, field))
            for field, validation in self._validations.items()
        )


def between(mi, ma):
    def wrap(n):
        try:
            return mi <= int(n) <= ma
        except ValueError:
            return False
    return wrap


def match_re(r):
    def wrap(s):
        return bool(re.fullmatch(r, s))
    return wrap


def validate_hgt(hgt):
    height, unit = hgt[:-2],hgt[-2:]
    if unit == "cm":
        return between(150, 193)(height)
    elif unit == "in":
        return between(59, 76)(height)
    else:
        return False


class SecurePassport(Passport):
    _validations = {
        'byr': between(1920, 2002),
        'iyr': between(2010, 2020),
        'eyr': between(2020, 2030),
        'hgt': validate_hgt,
        'hcl': match_re(r'#[0-9a-f]{6}'),
        'ecl': lambda s: s in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
        'pid': match_re(r'\d{9}'),
    }


def part_one(inp):
    return sum(Passport.from_batch(batch).is_valid
        for batch in inp.split('\n\n')
    )


def part_two(inp):
    return sum(SecurePassport.from_batch(batch).is_valid
        for batch in inp.split('\n\n')
    )


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
