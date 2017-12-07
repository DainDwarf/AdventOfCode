#!/usr/bin/python
from __future__ import print_function
import re

class Tower(object):
    def __init__(self, line):
        if '->' in line:
            head, deps = line.split('->')
            self.name = head.split()[0].strip()
            self.weight = int(head.split()[1].strip().strip('()'))
            self.deps = list(map(lambda s:s.strip(), deps.strip().split(', ')))
        else:
            self.name = line.split()[0].strip()
            self.weight = int(line.split()[1].strip().strip('()'))
            self.deps = []


    def __str__(self):
        if self.deps:
            return "{n} ({w}) -> {d}".format(n=self.name, w=self.weight, d=str(self.deps))
        else:
            return "{n} ({w})".format(n=self.name, w=self.weight)
        
def toTowerList(text):
    return list(map(Tower, text.strip().split('\n')))


def getHead(towerList):
    for t in towerList:
        if not any(map(lambda i: t.name in i.deps, towerList)):
            return t

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    example="""pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""

    print("Head of example towers is {t}".format(t=partOne(example)))


def partOne(inp):
    towers = toTowerList(inp)
    return getHead(towers)

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
        inp = options.input.read()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
