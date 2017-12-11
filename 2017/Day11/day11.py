#!/usr/bin/python3
from __future__ import print_function

#Ohohoh! Let's do some euclidean lattices!

#                    col, line
directions = { 'n' : ( 0,  2)
             , 'ne': ( 1,  1)
             , 'nw': (-1,  1)
             , 's' : ( 0, -2)
             , 'se': ( 1, -1)
             , 'sw': (-1, -1)
}

# That's an easy euclidean lattices. To go from one point to another,
# you can simply go east/west (using the correct north/south according to target position)
# and if you're not at the correct height, go north/south from here.


def walkPath(p):
    col=0
    line=0
    for d in p:
        c, l = directions[d]
        col +=c
        line +=l
    return (col, line)

def distance(position):
    # You need to at least walk that amount east (or west) to get to the position asked.
    ew_distance = abs(position[0])
    remaining_ns_distance = max(0, abs(position[1])-ew_distance)
    ns_steps = remaining_ns_distance // 2
    return ew_distance+ns_steps

def genPath(p):
    # Gives the successive positions during the path given by instructions.
    col=0
    line=0
    yield (0, 0)

    for d in p:
        c, l = directions[d]
        col +=c
        line +=l
        yield (col, line)

def genDistances(p):
    for pos in genPath(p):
        yield distance(pos)

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "ne,ne,ne"
    ex2 = "ne,ne,sw,sw"
    ex3 = "ne,ne,s,s"
    ex4 = "se,sw,se,sw,sw"

    print("Unit test for Part One.")
    print("Walk {inp} is at position {pos} and needs {res} steps".format(inp=ex1, pos=walkPath(ex1.split(',')), res=partOne(ex1)))
    print("Walk {inp} is at position {pos} and needs {res} steps".format(inp=ex2, pos=walkPath(ex2.split(',')), res=partOne(ex2)))
    print("Walk {inp} is at position {pos} and needs {res} steps".format(inp=ex3, pos=walkPath(ex3.split(',')), res=partOne(ex3)))
    print("Walk {inp} is at position {pos} and needs {res} steps".format(inp=ex4, pos=walkPath(ex4.split(',')), res=partOne(ex4)))

    print("")
    print("Unit test for Part Two.")


def partOne(inp):
    child_path = inp.split(',')
    child_pos = walkPath(child_path)
    return distance(child_pos)

def partTwo(inp):
    child_path = inp.split(',')
    return max(genDistances(child_path))

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
