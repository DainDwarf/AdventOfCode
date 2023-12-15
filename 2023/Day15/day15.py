#!/usr/bin/python3
import pytest


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("HASH", 52),
    ("rn=1", 30),
    ("cm-", 253),
    ("qp=3", 97),
    ("cm=2", 47),
    ("qp-", 14),
    ("pc=4", 180),
    ("ot=9", 9),
    ("ab=5", 197),
    ("pc-", 48),
    ("pc=6", 214),
    ("ot=7", 231),
])
def test_xmash(inp, exp):
    assert xmash(inp) == exp

def test_one():
    assert part_one("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7") == 1320

def xmash(string):
    ret = 0
    for c in string:
        ret += ord(c)
        ret *= 17
        ret %= 256
    return ret


def part_one(inp):
    return sum(xmash(step) for step in inp.split(','))


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
