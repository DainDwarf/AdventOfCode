#!/usr/bin/python3
from functools import reduce
import operator
import pytest

def mul(iterable):
    return reduce(operator.mul, iterable, 1)

# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = """
Time:      7  15   30
Distance:  9  40  200""".strip()

@pytest.mark.parametrize("inp, exp", [
    ((7, 9), 4),
    ((15, 40), 8),
    ((30, 200), 9),
    ((71530, 940200), 71503),
])
def test_count_better(inp, exp):
    assert count_better(*inp) == exp


def test_one():
    assert part_one(TEST_EXAMPLE) == 288


def test_two():
    assert part_two(TEST_EXAMPLE) == 71503


def count_better(time, distance):
    """Return the number of possible times we can press the button to beat the given distance.

    Since the distance is symmetric according to time, we can find the first time we beat the
    score and just compute the inner interval that will beat the distance."""
    for i in range(time):
        if i*(time-i) > distance:
            break
    return time-2*i+1


def part_one(inp):
    times, distances = inp.split('\n')
    times = [int(x) for x in times.split(':')[1].split()]
    distances = [int(x) for x in distances.split(':')[1].split()]
    return mul(count_better(*t) for t in zip(times, distances))


def part_two(inp):
    time, distance = inp.split('\n')
    time = int(time.replace(' ', '').split(':')[1])
    distance = int(distance.replace(' ', '').split(':')[1])
    return count_better(time, distance)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
