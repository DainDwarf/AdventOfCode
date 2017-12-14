#!/usr/bin/python3
from __future__ import print_function
from day10 import partTwo as knotHash


def hexToBin(s):
    return "{:0>128b}".format(int(s, 16))

class Disk(object):
    def __init__(self, key):
        self.grid = []
        for n in range(128):
            line_key = "{k}-{n}".format(k=key, n=n)
            self.grid.append(list(map(int, hexToBin(knotHash(line_key)))))

    def __str__(self):
        return '\n'.join(''.join(map(lambda n: '#' if n==1 else '.', line)) for line in self.grid)

    def getUsedCount(self):
        return sum(map(sum, self.grid))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = "flqrgnkx"

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    d = Disk(inp)
    return d.getUsedCount()

def partTwo(inp):
    pass

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
