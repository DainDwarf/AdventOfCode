#!/usr/bin/python3
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


@pytest.mark.parametrize("inp, exp", [
    ("41 48 83 86 17 | 83 86  6 31 17  9 48 53", 4),
    ("13 32 20 16 61 | 61 30 68 82 17 32 24 19", 2),
    (" 1 21 53 59 44 | 69 82 63 72 16 21 14  1", 2),
    ("41 92 73 84 69 | 59 84 76 51 58  5 54 83", 1),
    ("87 83 26 28 32 | 88 30 70 12 93 22 82 36", 0),
    ("31 18 13 56 72 | 74 77 10 23 35 67 36 11", 0),
])
def test_score(inp, exp):
    res = score(inp)
    assert res == exp


def test_one():
    assert part_one(TEST_EXAMPLE) == 13


@pytest.mark.skip
def test_two():
    assert part_two(TEST_EXAMPLE) == 30


def score(card):
    wins, nums = card.split('|')
    wins = [int(w) for w in wins.split()]
    nums = [int(n) for n in nums.split()]

    return sum(n in wins for n in nums)


def part_one(inp):
    ret = 0
    for line in inp.split('\n'):
        card = line.split(':')[1]
        if s := score(card):
            ret += 2**(s-1)
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
