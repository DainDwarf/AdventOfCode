#!/usr/bin/python3
from __future__ import print_function
from itertools import permutations

#Meh, salesman's problem, seriously? That's boring.
#So boring, I'm not even getting input as a source.

places = { 'AlphaCentauri'  : 0
         , 'Snowdin'        : 1
         , 'Tambi'          : 2
         , 'Faerun'         : 3
         , 'Norrath'        : 4
         , 'Straylight'     : 5
         , 'Tristram'       : 6
         , 'Arbre'          : 7
}

distances = { (0, 1): 66
            , (0, 2): 28
            , (0, 3): 60
            , (0, 4): 34
            , (0, 5): 34
            , (0, 6): 3
            , (0, 7): 108
            , (1, 2): 22
            , (1, 3): 12
            , (1, 4): 91
            , (1, 5): 121
            , (1, 6): 111
            , (1, 7): 71
            , (2, 3): 39
            , (2, 4): 113
            , (2, 5): 130
            , (2, 6): 35
            , (2, 7): 40
            , (3, 4): 63
            , (3, 5): 21
            , (3, 6): 57
            , (3, 7): 83
            , (4, 5): 9
            , (4, 6): 50
            , (4, 7): 60
            , (5, 6): 27
            , (5, 7): 81
            , (6, 7): 90
}

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    test_places = { 'London' : 0
                  , 'Dublin' : 1
                  , 'Belfast': 2
    }

    test_distances = { (0, 1): 464
                     , (0, 2): 518
                     , (1, 2): 141
    }

    print("Unit test for Part One.")
    print("Minimum road has distance {res}".format(res=partOne(test_places, test_distances)))

    print("")
    print("Unit test for Part Two.")
    print("Maximum road has distance {res}".format(res=partTwo(test_places, test_distances)))


def genRoutes(p, d):
    for path in permutations(range(len(p))):
        yield sum(d[(min(a, b), max(a, b))] for a, b in zip(path[:-1], path[1:]))

def partOne(p, d):
    return min(genRoutes(p, d))

def partTwo(p, d):
    return max(genRoutes(p, d))

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    options = args.parse_args()

    if options.test:
        UnitTest()
    print("Answer for part one is : {res}".format(res=partOne(places, distances)))
    print("Answer for part two is : {res}".format(res=partTwo(places, distances)))
