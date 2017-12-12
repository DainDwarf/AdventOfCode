#!/usr/bin/python3
from __future__ import print_function
import itertools

#Well, that's a common combinatory issue.... No way to do it except bruteforcing.

def genCombinations(containers):
    for size in range(1, len(containers)+1):
        yield from itertools.combinations(containers, size)


def genCombinationsFitting(containers, liters):
    for comb in genCombinations(containers):
        if sum(comb) == liters:
            yield comb

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = """20
15
10
5
5"""

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex, 25)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex, 25)))


def partOne(inp, liters):
    containers = list(map(int, inp.split('\n')))
    return len(list(genCombinationsFitting(containers, liters)))

def partTwo(inp, liters):
    containers = list(map(int, inp.split('\n')))
    fittings = list(genCombinationsFitting(containers, liters))
    smallest = min(map(len, fittings))
    count = 0
    for comb in fittings:
        if len(comb) == smallest:
            count += 1
    return count

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp, 150)))
        print("Answer for part two is : {res}".format(res=partTwo(inp, 150)))
