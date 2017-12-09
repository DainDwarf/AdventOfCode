#!/usr/bin/python3
from __future__ import print_function
import re


def cleanUp(s):
    escapes_re = r"!."
    comments_re = r"<[^>]*>"

    s = re.sub(escapes_re, "", s)
    s = re.sub(comments_re, "", s)

    return s

def yellScores(stream):
    """Yields scores from a cleaned_up stream."""
    current_nest=0
    for i in stream:
        if i == '{':
            current_nest += 1
            yield current_nest
        elif i == '}':
            current_nest -= 1 #But do not yield.

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "{}"
    ex2 = "{{{}}}"
    ex3 = "{{},{}}"
    ex4 = "{{{},{},{{}}}}"
    ex5 = "{<a>,<a>,<a>,<a>}"
    ex6 = "{{<ab>},{<ab>},{<ab>},{<ab>}}"
    ex7 = "{{<!!>},{<!!>},{<!!>},{<!!>}}"
    ex8 = "{{<a!>},{<a!>},{<a!>},{<ab>}}"


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
    print("Test {inp} gives {res}".format(inp=ex1, res=partTwo(ex1)))


def partOne(inp):
    stream = cleanUp(inp)
    return sum(yellScores(stream))

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
