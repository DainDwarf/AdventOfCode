#!/usr/bin/python3
from itertools import pairwise
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".strip()


@pytest.mark.parametrize("inp, exp", [
    ([0, 3, 6, 9, 12, 15], 18),
    ([1, 3, 6, 10, 15, 21], 28),
    ([10, 13, 16, 21, 30, 45], 68),
])
def test_next_in_sequence(inp, exp):
    res = next_in_sequence(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ([0, 3, 6, 9, 12, 15], -3),
    ([1, 3, 6, 10, 15, 21], 0),
    ([10, 13, 16, 21, 30, 45], 5),
])
def test_previous_in_sequence(inp, exp):
    res = previous_in_sequence(inp)
    assert res == exp


def test_part_one():
    assert part_one(TEST_EXAMPLE) == 114


def test_part_two():
    assert part_two(TEST_EXAMPLE) == 2


def generating_sequences(nums):
    """Returns a list of all sequences that generate the given nums sequence."""
    # Do not modify the input
    all_sequences = [nums[:]]
    while not all(i == 0 for i in all_sequences[-1]):
        all_sequences.append([j-i for i, j in pairwise(all_sequences[-1])])
    return all_sequences


def next_in_sequence(nums):
    all_sequences = generating_sequences(nums)

    step = 0
    for seq in all_sequences[::-1]:
        seq.append(seq[-1]+step)
        step = seq[-1]

    return all_sequences[0][-1]


def previous_in_sequence(nums):
    all_sequences = generating_sequences(nums)

    step = 0
    for seq in all_sequences[::-1]:
        seq.insert(0, seq[0]-step)
        step = seq[0]

    return all_sequences[0][0]


def part_one(inp):
    sequences = [list(map(int, line.split())) for line in inp.split('\n')]
    return sum(next_in_sequence(s) for s in sequences)


def part_two(inp):
    sequences = [list(map(int, line.split())) for line in inp.split('\n')]
    return sum(previous_in_sequence(s) for s in sequences)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
