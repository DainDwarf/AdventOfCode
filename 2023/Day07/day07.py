#!/usr/bin/python3
from collections import Counter
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".strip()

def test_one():
    assert part_one(TEST_EXAMPLE) == 6440


def test_two():
    assert part_two(TEST_EXAMPLE) == None


cards_value = {
    '2': 2, 
    '3': 3, 
    '4': 4, 
    '5': 5, 
    '6': 6, 
    '7': 7, 
    '8': 8, 
    '9': 9, 
    'T': 10, 
    'J': 11, 
    'Q': 12, 
    'K': 13, 
    'A': 14, 
}


def sorting_key(hand):
    hand_values = [cards_value[c] for c in hand]
    groups = sorted(Counter(hand).values(), reverse=True)
    main_group = groups[0]
    secondary_group = groups[1] if len(groups) > 1 else 1
    key = (main_group, secondary_group, *hand_values)
    return key


def part_one(inp):
    hands = []
    for line in inp.split('\n'):
        hand, bid = line.split()
        hands.append((hand, int(bid)))

    ret = 0
    for rank, (hand, bid) in enumerate(sorted(hands, key=lambda t: sorting_key(t[0])), 1):
        ret += rank*bid
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
