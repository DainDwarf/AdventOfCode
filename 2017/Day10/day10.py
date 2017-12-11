#!/usr/bin/python3
from __future__ import print_function
from functools import reduce

class Circle(object):
    def __init__(self, size):
        self.__l = list(range(size)) # Actual storage
        self.__cur = 0  # Current position for making knots.
        self.__skip = 0 # As per given algorithm.

    def __str__(self):
        return str(self.__l)

    def makeAKnot(self, leng):
        rev = list((self.__l+self.__l)[i] for i in range(self.__cur+leng-1, self.__cur-1, -1))
        for i in range(leng):
            self.__l[ (self.__cur+i)%len(self.__l) ] = rev[i]
        self.__cur = (self.__cur + leng + self.__skip) % len(self.__l)
        self.__skip += 1

    def __getitem__(self, i):
        return self.__l[i]

def KnotHash(s):
    lengths = list(map(ord, s)) + [17, 31, 73, 47, 23]
    c = Circle(256)
    for l in lengths*64:
        c.makeAKnot(l)
    dense = []
    for block in range(16):
        dense.append(reduce(lambda x, y: x^y, c[16*block:16*block+16]))

    to_hex = ''.join(map(lambda n: "{:0>2x}".format(n), dense))
    return to_hex




# That's handy, the Advent of Code gives unittests.
def UnitTest():
    testOne = Circle(5)

    print("Unit test for Part One.")
    print("Starting with circle {c}".format(c=testOne))
    testOne.makeAKnot(3)
    print("Aftert first knot (3) : {c}".format(c=testOne))
    testOne.makeAKnot(4)
    print("Aftert second knot (4) : {c}".format(c=testOne))
    testOne.makeAKnot(1)
    print("Aftert third knot (1) : {c}".format(c=testOne))
    testOne.makeAKnot(5)
    print("Aftert fourth knot (5) : {c}".format(c=testOne))

    ex1= ""
    ex2= "AoC 2017"
    ex3= "1,2,3"
    ex4= "1,2,4"

    print("")
    print("Unit test for Part Two.")
    print("The input {i} gives a hash of {r}".format(i=ex1, r=partTwo(ex1)))
    print("The input {i} gives a hash of {r}".format(i=ex2, r=partTwo(ex2)))
    print("The input {i} gives a hash of {r}".format(i=ex3, r=partTwo(ex3)))
    print("The input {i} gives a hash of {r}".format(i=ex4, r=partTwo(ex4)))


def partOne(inp):
    lengths = list(map(int, inp.strip().split(',')))
    c = Circle(256)
    for l in lengths:
        c.makeAKnot(l)
    return c[0] * c[1]

def partTwo(inp):
    return KnotHash(inp.strip())

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input list of lengths', type=str)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
