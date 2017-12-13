#!/usr/bin/python3
from __future__ import print_function

def scannerPosition(ran, clock):
    """Computes scanner position of a range 'ran' based on current clock."""
    return ran-1-abs(clock%((ran-1)*2)-(ran-1))%ran

def isCaught(layer, ran, start_clock=0):
    """Checks if you get caught by a layer of a certain range, if you start packet at start_clock."""
    return scannerPosition(ran, layer+start_clock) == 0

def getLayers(inp):
    """Returns a dictionary of layer: range."""
    return dict(map(int, l.strip().split(': ')) for l in inp.split('\n'))

def getSeverity(layers_dict, start_clock=0):
    """Returns the severity of a trip starting at start_clock."""
    return sum(layer*ran for layer, ran in layers_dict.items() if isCaught(layer, ran, start_clock))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = """0: 3
1: 2
4: 4
6: 4"""

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    return getSeverity(getLayers(inp), 0)

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
