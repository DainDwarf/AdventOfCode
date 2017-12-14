#!/usr/bin/python3
from __future__ import print_function
from day10 import partTwo as knotHash
import networkx as nx


def hexToBin(s):
    return "{:0>128b}".format(int(s, 16))

class Disk(object):
    def __init__(self, key):
        self.grid = []
        for n in range(128):
            line_key = "{k}-{n}".format(k=key, n=n)
            self.grid.append(list(map(int, hexToBin(knotHash(line_key)))))

    def __str__(self):
        return '\n'.join(''.join(map(lambda n: '#' if n==1 else '.', line)) for line in self.grid)

    def __getitem__(self, pos):
        line, col = pos
        if 128 > line >= 0 and 128 > col >= 0:
            return self.grid[pos[0]][pos[1]]
        else:
            return 0

    def getUsedCount(self):
        return sum(map(sum, self.grid))

    def getRegionCount(self):
        adjacency_graph = nx.Graph()
        for lin in range(128):
            for col in range(128):
                if self[(lin, col)] == 1:
                    adjacency_graph.add_node((lin, col))
                    if                      self[(lin  , col-1)] == 1:          # Left
                        adjacency_graph.add_edge((lin  , col-1), (lin, col))
                    if                      self[(lin-1, col  )] == 1:          # Down
                        adjacency_graph.add_edge((lin-1, col  ), (lin, col))
                    if                      self[(lin+1, col  )] == 1:          # Up
                        adjacency_graph.add_edge((lin+1, col  ), (lin, col))
                    if                      self[(lin  , col+1)] == 1:          # Right
                        adjacency_graph.add_edge((lin  , col+1), (lin, col))
        return len(list(nx.connected_components(adjacency_graph)))


# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = "flqrgnkx"

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    d = Disk(inp)
    return d.getUsedCount()

def partTwo(inp):
    d = Disk(inp)
    return d.getRegionCount()

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input', type=str)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
