#!/usr/bin/python3
from __future__ import print_function
from itertools import permutations
import re

def getPeopleSet(s):
    people = set()
    for line in s.split('\n'):
        people.add(line.split()[0])
    return people

def getRelationClique(s):
    """Parses input to get the gain/lose of each adjacency."""
    s = s.replace('lose ', '-')
    s = s.replace('gain ', '+')
    parsing_re = r"(\w+) would ([0-9+-]+) happiness units by sitting next to (\w+)\."
    clique = dict()
    for line in s.split('\n'):
        f, c, t = re.match(parsing_re, line).groups()
        clique[(f, t)] = int(c)
    return clique


def computeHappiness(perm, relations):
    """Given a permutation of people, compute the happiness generated."""
    cost = 0
    for l, r in zip(perm, perm[1:]+perm[:1]):
        cost += relations[(l, r)]
        cost += relations[(r, l)]
    return cost


def addYourself(people, clique):
    for p in people:
        clique[('Me', p)] = 0
        clique[(p, 'Me')] = 0
    people.add('Me')
    return people, clique

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
""".strip()

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    people = getPeopleSet(inp)
    relations = getRelationClique(inp)
    return max(computeHappiness(perm, relations) for perm in permutations(people))

def partTwo(inp):
    people = getPeopleSet(inp)
    relations = getRelationClique(inp)
    people, relations = addYourself(people, relations)
    return max(computeHappiness(perm, relations) for perm in permutations(people))

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
