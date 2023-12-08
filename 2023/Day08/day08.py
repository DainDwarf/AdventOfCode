#!/usr/bin/python3
from itertools import cycle
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE_1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

TEST_EXAMPLE_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

def test_one_1():
    assert part_one(TEST_EXAMPLE_1) == 2

def test_one_2():
    assert part_one(TEST_EXAMPLE_2) == 6

def test_two():
    assert part_two(TEST_EXAMPLE_2) == None


def part_one(inp):
    pattern, lines = inp.split('\n\n')
    pattern = [1 if c == 'R' else 0 for c in pattern]
    mapping = dict()
    for line in lines.split('\n'):
        node, tup = line.split(' = ')
        left, right = tup.strip('()').split(', ')
        mapping[node] = (left, right)

    pos = 'AAA'
    for step, direction in enumerate(cycle(pattern), 1):
        pos = mapping[pos][direction]
        if pos == 'ZZZ':
            break

    return step


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
