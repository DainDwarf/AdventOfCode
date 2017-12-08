#!/usr/bin/python3
from __future__ import print_function

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "(())"
    ex2 = "()()"
    ex3 = "((("
    ex4 = "(()(()("
    ex5 = "))((((("
    ex6 = "())"
    ex7 = "))("
    ex8 = ")))"
    ex9 = ")())())"

    print("Unit test for Part One.")
    print("Test {lisp} gives floor {res}".format(lisp=ex1, res=partOne(ex1)))
    print("Test {lisp} gives floor {res}".format(lisp=ex2, res=partOne(ex2)))
    print("Test {lisp} gives floor {res}".format(lisp=ex3, res=partOne(ex3)))
    print("Test {lisp} gives floor {res}".format(lisp=ex4, res=partOne(ex4)))
    print("Test {lisp} gives floor {res}".format(lisp=ex5, res=partOne(ex5)))
    print("Test {lisp} gives floor {res}".format(lisp=ex6, res=partOne(ex6)))
    print("Test {lisp} gives floor {res}".format(lisp=ex7, res=partOne(ex7)))
    print("Test {lisp} gives floor {res}".format(lisp=ex8, res=partOne(ex8)))
    print("Test {lisp} gives floor {res}".format(lisp=ex9, res=partOne(ex9)))

    ex10 = ')'
    ex11 = '()())'

    print("")
    print("Unit test for Part Two.")
    print("Test {lisp} gives index {res}".format(lisp=ex10, res=partTwo(ex10)))
    print("Test {lisp} gives index {res}".format(lisp=ex11, res=partTwo(ex11)))


def partOne(inp):
    return inp.count('(')-inp.count(')')

def partTwo(inp):
    l = 0
    for index, par in enumerate(inp, 1):
        if par == ')':
            l -= 1
        elif par == '(':
            l += 1
        else:
            raise RuntimeError('Unknown parenthes {off}'.format(off=par))
        if l < 0:
            return index



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
