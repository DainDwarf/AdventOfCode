#!/usr/bin/python
from __future__ import print_function
import re

class TowerParse(object):
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


class Tower(object):
    def __init__(self, name, weight, deps):
        self.name = name
        self.weight = weight
        self.deps = deps

    def __str__(self):
        if self.deps:
            return "{n} ({w}) -> {d}".format(n=self.name, w=self.weight, d=self.deps.name)
        else:
            return "{n} ({w})".format(n=self.name, w=self.weight)

    def __hash__(self):
        return hash(name)

    def realWeight(self):
        return self.weight + sum(map(lambda d: d.realWeight(), self.deps))

    def isBalanced(self):
        if self.deps:
            return all(map(lambda d: d.realWeight() == self.deps[0].realWeight(), self.deps))
        else:
            return True

def toTowerList(text):
    return list(map(TowerParse, text.strip().split('\n')))


def toTowerTree(text):
    towerParseList = toTowerList(text)
    parseDict = dict( (t.name, t) for t in towerParseList)

    def _turnToTree(parseNode):
        return Tower(parseNode.name, parseNode.weight, list(map(lambda n: _turnToTree(parseDict[n]), parseNode.deps)))

    head = getHead(towerParseList)
    return _turnToTree(head)

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
    partTwo(example)


def partOne(inp):
    towers = toTowerList(inp)
    return getHead(towers)

def partTwo(inp):
    tree = toTowerTree(inp)
    allNodes = []

    def _addNodes(node):
        allNodes.append(node)
        for n in node.deps:
            _addNodes(n)
    _addNodes(tree)

    for n in allNodes:
        if not n.isBalanced() and all(map(lambda d: d.isBalanced(), n.deps)):
            print("Node {name} is wrong!".format(name=n.name))
            for d in n.deps:
                print("Dependancy {name} of weight {w} has realweight {r}".format(name=d.name, w=d.weight, r=d.realWeight()))



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
