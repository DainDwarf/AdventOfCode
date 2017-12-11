#!/usr/bin/python3
from __future__ import print_function
from itertools import groupby

def lookAndSay(s):
    ret = ""
    for n, g in groupby(s):
        ret += "{g}{n}".format(g=len(list(g)), n=n)
    return ret


# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "1"
    ex2 = "11"
    ex3 = "21"
    ex4 = "1211"
    ex5 = "111221"

    print("Unit test for Part One.")
    print("LookAndSay on {inp} gives {res}".format(inp=ex1, res=lookAndSay(ex1)))
    print("LookAndSay on {inp} gives {res}".format(inp=ex2, res=lookAndSay(ex2)))
    print("LookAndSay on {inp} gives {res}".format(inp=ex3, res=lookAndSay(ex3)))
    print("LookAndSay on {inp} gives {res}".format(inp=ex4, res=lookAndSay(ex4)))
    print("LookAndSay on {inp} gives {res}".format(inp=ex5, res=lookAndSay(ex5)))

    print("")
    print("Unit test for Part Two.")


def partOne(inp):
    for i in range(40):
        inp = lookAndSay(inp)
    return len(inp)

def partTwo(inp):
    for i in range(50):
        inp = lookAndSay(inp)
    return len(inp)

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
