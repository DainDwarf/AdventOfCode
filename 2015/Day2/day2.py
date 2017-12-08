#!/usr/bin/python3
from __future__ import print_function

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "2x3x4"
    ex2 = "1x1x10"

    print("Unit test for Part One.")
    print("Test {lisp} requires {res} square feet".format(lisp=ex1, res=wrapping(ex1)))
    print("Test {lisp} requires {res} square feet".format(lisp=ex2, res=wrapping(ex2)))

    print("Unit test for Part Two.")
    print("Test {lisp} requires {res} feet of ribbon".format(lisp=ex1, res=ribbon(ex1)))
    print("Test {lisp} requires {res} feet of ribbon".format(lisp=ex2, res=ribbon(ex2)))


def ribbon(inp):
    l, w, h = sorted(map(int, inp.split('x')))
    return l+l+w+w+l*w*h


def wrapping(inp):
    l, w, h = map(int, inp.split('x'))
    return 2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, h*l)

def partOne(inp):
    return sum(map(wrapping, inp.split('\n')))

def partTwo(inp):
    return sum(map(ribbon, inp.split('\n')))

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
