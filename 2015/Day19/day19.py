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

    print("")
    print("Unit test for Part Two.")
    # print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(molecule, rules_str):
    rules = getAllRules(rules_str)
    return len(set(genAllSubstitutions(molecule, rules)))

def partTwo(inp):
    pass

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
        # print("Answer for part two is : {res}".format(res=partTwo(inp)))
