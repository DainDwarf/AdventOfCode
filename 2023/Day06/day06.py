#!/usr/bin/python3
from functools import reduce
import operator
import pytest

def mul(iterable):
    return reduce(operator.mul, iterable, 1)

TEST_EXAMPLE = """
Time:      7  15   30
Distance:  9  40  200""".strip()

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ((7, 9), 4),
    ((15, 40), 8),
    ((30, 200), 9),
])
def test_count_better(inp, exp):
    assert count_better(*inp) == exp

def test_one():
    assert part_one(TEST_EXAMPLE) == 288


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


def count_better(time, distance):
    """Not even doing math for this one yet."""
    return sum(i*(time-i) > distance for i in range(time))


def part_one(inp):
    times, distances = inp.split('\n')
    times = [int(x) for x in times.split(':')[1].split()]
    distances = [int(x) for x in distances.split(':')[1].split()]
    return mul(count_better(*t) for t in zip(times, distances))


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
