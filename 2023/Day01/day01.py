#!/usr/bin/python3
import pytest


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""", 142)
])
def test_one(inp, exp):
    res = part_one(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""", 281)
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


def part_one(inp):
    ret = 0
    for line in inp.split('\n'):
        nums = [int(c) for c in line if c in "0123456789"]
        ret += nums[0]*10+nums[-1]
    return ret


ALL_NUMS = [
    ('0', 0),
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6),
    ('7', 7),
    ('8', 8),
    ('9', 9),
    ('one', 1),
    ('two', 2),
    ('three', 3),
    ('four', 4),
    ('five', 5),
    ('six', 6),
    ('seven', 7),
    ('eight', 8),
    ('nine', 9),
]
def part_two(inp):
    ret = 0
    for line in inp.split('\n'):
        l_pos = r_pos = l_val = r_val = -1
        for word, value in ALL_NUMS:
            if word in line:
                if (pos := line.find(word)) < l_pos or l_pos == -1:
                    l_val = value
                    l_pos = pos
                if (pos := line.rfind(word)) > r_pos or r_pos == -1:
                    r_val = value
                    r_pos = pos
        line_val = l_val*10+r_val
        ret += line_val
    return ret


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
