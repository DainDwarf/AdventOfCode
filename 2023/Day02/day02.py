#!/usr/bin/python3
from collections import defaultdict
from enum import StrEnum, auto
import pytest


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
    ("1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
    ("8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", False),
    ("1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", False),
    ("6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True),
])
def test_game_is_valid(inp, exp):
    res = game_is_valid(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("3 blue, 4 red", True),
    ("3 green, 4 blue, 1 red", True),
    ("8 green, 6 blue, 20 red", False),
    ("5 blue, 4 red, 13 green", True),
    ("3 green, 15 blue, 14 red", False),
    ("6 red, 1 blue, 3 green", True),
])
def test_set_is_valid(inp, exp):
    res = set_is_valid(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


class Color(StrEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


def to_set(inp: str):
    ret = defaultdict(int)
    for cube in inp.split(', '):
        num, color = cube.split()
        num = int(num)
        color = Color(color)
        ret[color] = num
    return ret


def set_is_valid(inp:str):
    check = to_set(inp)
    print(check)
    return check[Color.RED] <= 12 and \
           check[Color.GREEN] <= 13 and \
           check[Color.BLUE] <= 14

    
def game_is_valid(line):
    all_sets = line.split('; ')
    return all(set_is_valid(s) for s in all_sets)


def part_one(inp):
    ret = 0
    for line in inp.split('\n'):
        game_num, line = line.split(': ')
        game_num = int(game_num.split()[1])
        ret += game_num if game_is_valid(line) else 0
    return ret


def part_two(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
