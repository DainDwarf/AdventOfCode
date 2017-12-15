#!/usr/bin/python3
from __future__ import print_function
import re

def genSubstitutions(molecule, fr, to):
    """Generates all substitutions you can get from a replacement rule 'fr => to' on given molecule."""
    for m in re.finditer(fr, molecule):
        yield molecule[:m.start()] + to + molecule[m.end():]

def genAllSubstitutions(molecule, rules):
    for fr, to in rules:
        yield from genSubstitutions(molecule, fr, to)

def getAllRules(inp):
    return list(l.split(' => ') for l in inp.split('\n'))

def getAllReverseRules(inp):
    return list(map(lambda l: (l.strip().split(' => ')[1], l.strip().split(' => ')[0]),inp.split('\n')))

def Levenshtein(a, b):
    """Computes Levenshtein distance, to use as heuristic for Astar.

    Iterative algorithm from Wikipedia."""
    v0 = list(range(len(b)+1))
    v1 = list(range(len(b)+1)) # Or whatever.

    for i in range(len(a)):
        v1[0] = i + 1

        for j in range(len(b)):
            deletionCost = v0[j + 1] + 1
            insertionCost = v1[j] + 1
            substitutionCost = v0[j] if a[i] == b[j] else v0[j]+1
            v1[j + 1] = min(deletionCost, insertionCost, substitutionCost)

        v1, v0 = v0, v1
    return v0[len(b)]


def AStar(start, end, rules):
    closedSet = set()
    gScore = {start: 0}
    fScore = {start: Levenshtein(start, end)}

    while fScore:
        current, _ = min(fScore.items(), key=lambda i:i[1])
        if current == end:
            return gScore[current]

        fScore.pop(current)
        closedSet.add(current)
        for neighbor in set(genAllSubstitutions(current, rules)):
            if neighbor in closedSet:
                continue

            tentative_gScore = gScore[current] + 1
            if neighbor in gScore and tentative_gScore >= gScore[neighbor]:
                continue

            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = tentative_gScore + Levenshtein(neighbor, end)

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex_rules = """H => HO
H => OH
O => HH"""
    ex1 = "HOH"
    ex2 = "HOHOHO"

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partOne(ex1, ex_rules)))
    print("Test {inp} gives {res}".format(inp=ex2, res=partOne(ex2, ex_rules)))

    ex2_rules = """e => H
e => O
H => HO
H => OH
O => HH"""

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partTwo(ex1, ex2_rules)))
    print("Test {inp} gives {res}".format(inp=ex2, res=partTwo(ex2, ex2_rules)))


def partOne(molecule, rules_str):
    rules = getAllRules(rules_str)
    return len(set(genAllSubstitutions(molecule, rules)))

def partTwo(molecule, rules_str):
    # It goes much faster to go in reverse, for this.
    rules = getAllReverseRules(rules_str)
    return AStar(molecule, 'e', rules)

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file (for rules only)', type=FileType('r'))
    args.add_argument("-m", "--molecule", help='Your input molecule', type=str)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(options.molecule, inp)))
        print("Answer for part two is : {res}".format(res=partTwo(options.molecule, inp)))
