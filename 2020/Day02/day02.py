#!/usr/bin/python3
from collections import Counter
import pytest
import re


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("1-3 a: abcde", True),
    ("1-3 b: cdefg", False),
    ("2-9 c: ccccccccc", True),
])
def test_line_is_valid(inp, exp):
    res = line_is_valid(inp)
    assert res == exp


def test_one():
    inp = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
    assert part_one(inp) == 2


@pytest.mark.parametrize("inp, exp", [
    ("1-3 a: abcde", True),
    ("1-3 b: cdefg", False),
    ("2-9 c: ccccccccc", False),
])
def test_line_is_valid(inp, exp):
    res = new_line_is_valid(inp)
    assert res == exp

@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    inp = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
    assert part_one(inp) == 1


class PasswordPolicy:

    def __init__(self, minimum, maximum, letter):
        self.minimum = minimum
        self.maximum = maximum
        self.letter = letter

    @classmethod
    def from_description(cls, desc):
        """Parse the password policy description."""
        mini, maxi, l = re.match(r"(\d+)-(\d+) ([a-z])", desc).groups()
        return cls(int(mini), int(maxi), l)

    def password_is_valid(self, password):
        count = Counter(password)
        return self.minimum <= count[self.letter] <= self.maximum


class NewPasswordPolicy(PasswordPolicy):
    def password_is_valid(self, password):
        return (password[self.minimum-1] == self.letter and password[self.maximum-1] != self.letter) \
            or (password[self.minimum-1] != self.letter and password[self.maximum-1] == self.letter)


def line_is_valid(line):
    policy_desc, password = line.strip().split(': ')
    policy = PasswordPolicy.from_description(policy_desc)
    return policy.password_is_valid(password)


def new_line_is_valid(line):
    policy_desc, password = line.strip().split(': ')
    policy = NewPasswordPolicy.from_description(policy_desc)
    return policy.password_is_valid(password)


def part_one(inp):
    return sum(line_is_valid(line) for line in inp.split('\n'))


def part_two(inp):
    return sum(new_line_is_valid(line) for line in inp.split('\n'))


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
