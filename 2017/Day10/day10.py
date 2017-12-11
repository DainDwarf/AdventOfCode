#!/usr/bin/python3
from __future__ import print_function

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

    print("")
    print("Unit test for Part Two.")


def partOne(inp):
    c = Circle(256)
    for l in inp:
        c.makeAKnot(l)
    return c[0] * c[1]

def partTwo(inp):
    pass

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
        print("Answer for part one is : {res}".format(res=partOne(list(map(int, inp.strip().split(','))))))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
