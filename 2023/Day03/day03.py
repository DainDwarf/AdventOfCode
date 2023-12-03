#!/usr/bin/python3
from collections import defaultdict
import re
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

def test_one():
    assert part_one(TEST_EXAMPLE) == 4361

def test_two():
    assert part_two(TEST_EXAMPLE) == 467835


def engine_with_borders(inp):
    """Returns a list of lines representing the engine, with extra '.' around"""
    lines = inp.split('\n')
    engine = list('.'+l+'.' for l in lines)
    border = '.'*len(engine[0])
    engine.insert(0, border)
    engine.append(border)
    return engine


def all_parts(engine):
    for i, line in enumerate(engine):
        for m in re.finditer(r"[0-9]+", line):
            neighbors = engine[i-1][m.start()-1:m.end()+1] \
                      + line[m.start()-1] + line[m.end()] \
                      + engine[i+1][m.start()-1:m.end()+1]
            if any(c not in "0123456789." for c in neighbors):
                yield int(m[0])


def all_gear_parts(engine):
    """Yields tuples (i, j, part) corresponding to each gear position (i, j) and a part number next to it.

    The same coordinates (i, j) can be yield more than once, but each part will only be yield once."""
    for i, line in enumerate(engine):
        for m in re.finditer(r"[0-9]+", line):
            part = int(m[0])
            if line[m.start()-1] == '*':
                yield (i, m.start()-1, part)
            if line[m.end()] == '*':
                yield (i, m.end(), part)
            for j in range(m.start()-1, m.end()+1):
                if engine[i-1][j] == '*':
                    yield (i-1, j, part)
                if engine[i+1][j] == '*':
                    yield (i+1, j, part)
    

def part_one(inp):
    return sum(all_parts(engine_with_borders(inp)))


def part_two(inp):
    engine = engine_with_borders(inp)
    gear_groups = defaultdict(list)
    for i, j, part in all_gear_parts(engine):
        gear_groups[(i, j)].append(part)

    ret = 0
    for parts in gear_groups.values():
        if len(parts) == 2:
            ret += parts[0]*parts[1]
    return ret


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
