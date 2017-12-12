#!/usr/bin/python3
from __future__ import print_function
#Well, it's a graph problem, so let's use a graph library.
import networkx as nx


def inputToGraph(inp):
    G = nx.Graph()
    for line in inp.split('\n'):
        v, l = line.strip().split(' <-> ')
        l = l.split(', ')
        for v2 in l:
            G.add_edge(int(v), int(v2))
    return G



# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    G = inputToGraph(inp)
    for s in nx.connected_components(G):
        if 0 in s:
            return len(s)

def partTwo(inp):
    G = inputToGraph(inp)
    return len(list(nx.connected_components(G)))

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
