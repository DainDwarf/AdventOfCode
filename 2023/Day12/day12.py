#!/usr/bin/python3
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
    dots_number = len(line) - sum(groups)

    # Iterate through all dots repartitions possible and count valid matches.
    # TODO: Choose between dots or sharp repartitions depending on what is smaller
    liberties = dots_number - line.count('.')

    ret = 0
    count = line.count('?')
    for repartition in range(2**count):
        test_line = line
        repartition = [int(b) for b in f"{repartition:0>{count}b}"]
        for bit in repartition:
            test_line = test_line.replace('?', '.' if bit else '#', 1)
        if group_lengths(test_line) == groups:
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
