#!/usr/bin/python
from __future__ import print_function
from itertools import *

def partOne(inp):
    return sum(map(lambda i, n: int(i) if i==n else 0, inp, inp[1:] + inp[:1]))

def partTwo(inp):
    return sum(map(lambda i, n: int(i) if i==n else 0, inp, inp[len(inp)/2:] + inp[:len(inp)/2]))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    print("Part one unit testing:")
    print("1122 produces {res}".format(res=partOne("1122")))
    print("1111 produces {res}".format(res=partOne("1111")))
    print("1234 produces {res}".format(res=partOne("1234")))
    print("91212129 produces {res}".format(res=partOne("91212129")))

    print("\nPart two unit testing:")
    print("1212 produces {res}".format(res=partTwo("1212")))
    print("1221 produces {res}".format(res=partTwo("1221")))
    print("123425 produces {res}".format(res=partTwo("123425")))
    print("123123 produces {res}".format(res=partTwo("123123")))
    print("12131415 produces {res}".format(res=partTwo("12131415")))

if __name__ == '__main__':
    from argparse import ArgumentParser

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("input", help='Your input')
    options = args.parse_args()

    if options.test:
        UnitTest()

    print("Answer for part one is : {res}".format(res=partOne(options.input)))
    print("Answer for part two is : {res}".format(res=partTwo(options.input)))

