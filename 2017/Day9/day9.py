#!/usr/bin/python3
from __future__ import print_function
import re

escapes_re = r"!."
comments_re = r"<[^>]*>"

def cleanUp(s):
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

    ex10 = '<>'
    ex11 = '<random characters>'
    ex12 = '<<<<>'
    ex13 = '<{!>}>'
    ex14 = '<!!>'
    ex15 = '<!!!>>'
    ex16 = '<{o"i!a,<{i<a>'
    ex17 = 'eibunbeiruvb<{o"i!a,<{i<a>zeivuneiun<{o"i!a,<{i<a>efibyueiyubeiu'


    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex10, res=partTwo(ex10)))
    print("Test {inp} gives {res}".format(inp=ex11, res=partTwo(ex11)))
    print("Test {inp} gives {res}".format(inp=ex12, res=partTwo(ex12)))
    print("Test {inp} gives {res}".format(inp=ex13, res=partTwo(ex13)))
    print("Test {inp} gives {res}".format(inp=ex14, res=partTwo(ex14)))
    print("Test {inp} gives {res}".format(inp=ex15, res=partTwo(ex15)))
    print("Test {inp} gives {res}".format(inp=ex16, res=partTwo(ex16)))
    print("Test {inp} gives {res}".format(inp=ex17, res=partTwo(ex17)))


def partOne(inp):
    stream = cleanUp(inp)
    return sum(yellScores(stream))


class CountGarbage(object):
    def __init__(self):
        self.count = 0
    def __call__(self, match):
        self.count += match.span()[1] - match.span()[0] -2
    def getCount(self):
        return self.count

def partTwo(inp):
    stream = re.sub(escapes_re, "", inp)
    counter = CountGarbage()
    # The following does not correctly uses closure for 'garbage' variable.
    # I suspect it might be a bug in python/re?
    # garbage = 0
    # def _count_garbage(match):
    #     garbage += len(match)
    #     return ""
    re.sub(comments_re, counter, stream)
    return counter.getCount()

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
