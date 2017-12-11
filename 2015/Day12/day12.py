#!/usr/bin/python3
from __future__ import print_function
import re

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = '[1,2,3]'
    ex2 = '{"a":2,"b":4}'
    ex3 = '[[[3]]]'
    ex4 = '{"a":{"b":4},"c":-1}'
    ex5 = '{"a":[-1,1]}'
    ex6 = '[-1,{"a":1}]'
    ex7 = '[]'
    ex8 = '{}'

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partOne(ex1)))
    print("Test {inp} gives {res}".format(inp=ex2, res=partOne(ex2)))
    print("Test {inp} gives {res}".format(inp=ex3, res=partOne(ex3)))
    print("Test {inp} gives {res}".format(inp=ex4, res=partOne(ex4)))
    print("Test {inp} gives {res}".format(inp=ex5, res=partOne(ex5)))
    print("Test {inp} gives {res}".format(inp=ex6, res=partOne(ex6)))
    print("Test {inp} gives {res}".format(inp=ex7, res=partOne(ex7)))
    print("Test {inp} gives {res}".format(inp=ex8, res=partOne(ex8)))

    print("")
    print("Unit test for Part Two.")


def partOne(inp):
    num_re = r"[0-9-]+"
    return sum(map(int, re.findall(num_re, inp)))

def partTwo(inp):
    pass

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
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
