#!/usr/bin/python3
from itertools import count, repeat, accumulate, chain

#Dealing with infinite lists all along, I should use some haskell instead.

class Vect(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vect(self.x + other.x, self.y+other.y)

    def __str__(self):
        return '({x}, {y})'.format(x=self.x, y=self.y)

    def __repr__(self):
        return '({x}, {y})'.format(x=self.x, y=self.y)

RIGHT   = Vect( 0,  1)
LEFT    = Vect( 0, -1)
UP      = Vect( 1,  0)
DOWN    = Vect(-1,  0)


def genDirections():
    """Gives the vectors to generate the spiral, by giving each direction in correct order.

    To determine when to turn, you can observe that the spiral goes like this:
        1 right, 1 up
        2 left, 2 down
        3 right, 3 up
        4 left, 4 down
        ...
    """

    for i in count(1, 2):
        yield from repeat(RIGHT, i)
        yield from repeat(UP, i)
        yield from repeat(LEFT, i+1)
        yield from repeat(DOWN, i+1)

def genPositions():
    pos = Vect(0, 0)
    for direction in genDirections():
        yield pos
        pos += direction

def getPosition(num):
    '''Returns the position of a given number in the spiral.'''
    if num <= 0:
        raise RuntimeError("Number below 0 are not permitted!")

    for current, pos in enumerate(genPositions(), 1):
        if current == num:
            return pos

def partOne(inp):
    pos = getPosition(inp)
    return abs(pos.x) + abs(pos.y)

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    print("Part one unit testing.")
    print("Path from 1 has length {res}".format(res=partOne(1)))
    print("Path from 12 has length {res}".format(res=partOne(12)))
    print("Path from 23 has length {res}".format(res=partOne(23)))
    print("Path from 1024 has length {res}".format(res=partOne(1024)))

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input number', type=int)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        print("Path for part one has length {res}".format(res=partOne(options.input)))
