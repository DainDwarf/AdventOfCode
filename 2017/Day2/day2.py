#!/usr/bin/python
from __future__ import print_function
from itertools import permutations

def partOne(inp):
    def diff(line):
        nums = map(int, line.strip().split())
        return max(nums) - min(nums)

    return sum(map(diff, inp.strip().split('\n')))

def partTwo(inp):
    def getCorrectDivision(line):
        nums = map(int, line.strip().split())
        for a, b in permutations(nums, 2):
            if a%b == 0:
                return a/b
        return 0
    return sum(map(getCorrectDivision, inp.strip().split('\n')))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    print("Part one unit testing : {res}".format(res=partOne('''5 1 9 5
7 5 3
2 4 6 8''')))

    print("Part two unit testing : {res}".format(res=partTwo('''5 9 2 8
9 4 7 3
3 8 6 5''')))

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))

