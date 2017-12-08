#!/usr/bin/python3
from __future__ import print_function
from hashlib import md5
from itertools import count

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "abcdef"
    ex2 = "pqrstuv"

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partOne(ex1)))
    print("Test {inp} gives {res}".format(inp=ex2, res=partOne(ex2)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partTwo(ex1)))
    print("Test {inp} gives {res}".format(inp=ex2, res=partTwo(ex2)))


def partOne(inp):
    for i in count():
        if md5(bytes(inp+str(i), 'ascii')).hexdigest().startswith('00000'):
            return i


def partTwo(inp):
    for i in count():
        if md5(bytes(inp+str(i), 'ascii')).hexdigest().startswith('000000'):
            return i

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input', type=str)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
