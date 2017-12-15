#!/usr/bin/python3
from __future__ import print_function
from itertools import count
from sympy import divisors

def genDivisors(num):
    """Non-optimized algorithm to output all divisors of a number."""
    for i in range(1, num+1):
        if num%i == 0:
            yield i

def presents(house_num):
    return 10*sum(divisors(house_num))

def lazyPresents(house_num):
    return 11*sum( d for d in divisors(house_num) if d*50 >= house_num)

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    print("Unit test for Part One.")
    print("House {inp} gets {res} presents".format(inp=1, res=presents(1)))
    print("House {inp} gets {res} presents".format(inp=4, res=presents(4)))

    print("")
    print("Unit test for Part Two.")


def partOne(inp):
    for i in count():
        if presents(i) >= inp:
            return i

def partTwo(inp):
    for i in count():
        if lazyPresents(i) >= inp:
            return i

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input', type=int)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
