#!/usr/bin/python3
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE_1 = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.""".strip()

TEST_EXAMPLE_2 = """
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".strip()

def test_vertical_reflexion():
    assert vertical_reflexion(TEST_EXAMPLE_1) == 5
    assert vertical_reflexion(TEST_EXAMPLE_2) == 0

def test_horizontal_reflexion():
    assert horizontal_reflexion(TEST_EXAMPLE_1) == 0
    assert horizontal_reflexion(TEST_EXAMPLE_2) == 4


def transpose(lines):
    """Returns a new list of lines that is the transposed of input"""
    return list(map(str, zip(*lines)))


def vertical_reflexion(block):
    lines = transpose(block.split('\n'))
    return horizontal_reflexion('\n'.join(lines))


def horizontal_reflexion(block):
    lines = block.split('\n')
    for i in range(len(lines)):
        if all(up == down for up, down in zip(lines[i-1::-1], lines[i:])):
            return i
    return 0


def part_one(inp):
    ret = 0
    for block in inp.split('\n\n'):
        ret += 100*horizontal_reflexion(block)+vertical_reflexion(block)
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
