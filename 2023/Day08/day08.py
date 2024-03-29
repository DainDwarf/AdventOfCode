#!/usr/bin/python3
from itertools import cycle
import math
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

TEST_EXAMPLE_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

def test_one_1():
    assert part_one(TEST_EXAMPLE_1) == 2

def test_one_2():
    assert part_one(TEST_EXAMPLE_2) == 6

def test_two():
    assert part_two(TEST_EXAMPLE_3) == 6


def parse_input(inp):
    """Return the pattern to follow and the mapping of nodes."""
    pattern, lines = inp.split('\n\n')
    pattern = [1 if c == 'R' else 0 for c in pattern]
    mapping = dict()
    for line in lines.split('\n'):
        node, tup = line.split(' = ')
        left, right = tup.strip('()').split(', ')
        mapping[node] = (left, right)
    return pattern, mapping


def part_one(inp):
    pattern, mapping = parse_input(inp)

    pos = 'AAA'
    for step, direction in enumerate(cycle(pattern), 1):
        pos = mapping[pos][direction]
        if pos == 'ZZZ':
            break

    return step


def part_two(inp):
    pattern, mapping = parse_input(inp)

    all_pos = [p for p in mapping.keys() if p[-1] == 'A']
    first_Z = [0]*len(all_pos)
    second_Z = [0]*len(all_pos)
    for step, direction in enumerate(cycle(pattern), 1):
        all_pos = [mapping[p][direction] for p in all_pos]
        for i, p in enumerate(all_pos):
            if p[-1] == 'Z':
                if first_Z[i] == 0:
                    first_Z[i] = step
                elif second_Z[i] == 0:
                    second_Z[i] = step
        if all(x != 0 for x in second_Z):
            break

    cycle_lengths = [s-f for f, s in zip(first_Z, second_Z)]
    # In the general case, the 'Z' node could not have the same behavior
    # than the 'A' node, resulting in extra steps to fall into each cycles.
    # However, it seems AoC is kind today and we don't need that extra steps counting.
    # Making sure it works with an assert, though.
    assert cycle_lengths == first_Z
    return math.lcm(*cycle_lengths)



if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
