#!/usr/bin/python3
from __future__ import print_function
from itertools import chain

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = ">"
    ex2 = "^>v<"
    ex3 = "^v^v^v^v^v"

    print("Unit test for Part One.")
    print("Test {lisp} delivers {res} houses".format(lisp=ex1, res=partOne(ex1)))
    print("Test {lisp} delivers {res} houses".format(lisp=ex2, res=partOne(ex2)))
    print("Test {lisp} delivers {res} houses".format(lisp=ex3, res=partOne(ex3)))

    ex4 = "^v"

    print("")
    print("Unit test for Part Two.")
    print("Test {lisp} delivers {res} houses".format(lisp=ex4, res=partTwo(ex4)))
    print("Test {lisp} delivers {res} houses".format(lisp=ex2, res=partTwo(ex2)))
    print("Test {lisp} delivers {res} houses".format(lisp=ex3, res=partTwo(ex3)))




def walk(directions):
    current_line = 0
    current_column = 0

    yield (current_line, current_column)

    for d in directions:
        if d == '^':
            current_line += 1
        elif d == 'v':
            current_line -= 1
        elif d == '<':
            current_column -= 1
        elif d == '>':
            current_column += 1
        else:
            raise RuntimeError("Unknown direction d".format(d=d))
        yield (current_line, current_column)


def partOne(inp):
    return len(set(walk(inp)))

def partTwo(inp):
    return len(set(chain(walk(inp[::2]), walk(inp[1::2]))))

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
