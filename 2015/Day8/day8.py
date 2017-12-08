#!/usr/bin/python3
from __future__ import print_function

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    # Beware, we need some escaping of escaping sequences to test!
    ex1 = '""'
    ex2 = '"abc"'
    ex3 = '"aaa\\"aaa"'
    ex4 = '"\\x27"'

    print("Unit test for Part One.")
    print("Test {inp} has representation's length {r} but in-memory length {m}".format(inp=ex1, r=len(ex1), m=len(eval(ex1))))
    print("Test {inp} has representation's length {r} but in-memory length {m}".format(inp=ex2, r=len(ex2), m=len(eval(ex2))))
    print("Test {inp} has representation's length {r} but in-memory length {m}".format(inp=ex3, r=len(ex3), m=len(eval(ex3))))
    print("Test {inp} has representation's length {r} but in-memory length {m}".format(inp=ex4, r=len(ex4), m=len(eval(ex4))))

    print("All four inputs gives total difference {res}".format(res=partOne('\n'.join([ex1, ex2, ex3, ex4]))))

    print("")
    print("Unit test for Part Two.")
    print("All four inputs need {res} more to encode.".format(res=partTwo('\n'.join([ex1, ex2, ex3, ex4]))))


def partOne(inp):
    return sum(len(s) - len(eval(s)) for s in inp.split('\n'))

def partTwo(inp):
    return sum(s.count('"') + s.count('\\') + 2 for s in inp.split('\n'))

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
