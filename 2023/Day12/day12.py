#!/usr/bin/python3
from itertools import combinations
import re
import pytest


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 4),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
    ("????.#...#... 4,1,1", 1),
    ("????.######..#####. 1,6,5", 4),
    ("?###???????? 3,2,1", 10),
])
def test_count_arrangements(inp, exp):
    assert count_arrangements(inp) == exp


def group_lengths(line, char='#'):
    """Return the group lengths of consecutive characters in the line."""

    assert len(char) == 1, f"Can only group with single characters, not {char}"
    return [len(m) for m in re.findall(f"[{char}]+", line)]


def count_arrangements(line):
    line, groups = line.split(' ')
    groups = [int(x) for x in groups.split(',')]

    # Iterate through all dots repartitions possible and count valid matches.
    # TODO: Choose between dots or sharp repartitions depending on what is smaller
    dots_count = len(line) - sum(groups)
    liberties = dots_count - line.count('.')
    qmark_positions = [i for i, c in enumerate(line) if c == '?']

    ret = 0
    for repartition in combinations(qmark_positions, liberties):
        test_line = list(line)
        for i, c in enumerate(test_line):
            if c == '?':
                test_line[i] = '.' if i in repartition else '#'
        if group_lengths(''.join(test_line)) == groups:
            ret += 1
    return ret


def part_one(inp):
    return sum(count_arrangements(line) for line in inp.split('\n'))


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
