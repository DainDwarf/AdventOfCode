#!/usr/bin/python3
from __future__ import print_function
import networkx as nx


class LicenseTree(object):
    def __init__(self):
        self.G = nx.DiGraph()

    @classmethod
    def fromDescription(cls, desc):
        self = cls()
        desc = list(map(int, desc.split()))
        current_children = []
        node_num = 0

        while desc:
            node_num += 1
            num_child = desc.pop(0)
            num_meta = desc.pop(0)

            if num_child == 0:  # Leaf
                payload = [desc.pop(0) for _ in range(num_meta)]
                self.G.add_node(node_num, payload=payload)
                pile_num = node_num
                while current_children: #Or break if there are more leaves to deal with.
                    parent, parent_child, parent_meta = current_children.pop(-1)
                    self.G.add_edge(parent, pile_num)
                    if parent_child > 1:
                        current_children.append((parent, parent_child-1, parent_meta))
                        break
                    else:
                        payload = [desc.pop(0) for _ in range(parent_meta)]
                        self.G.add_node(parent, payload=payload)
                        pile_num = parent
            else:   #Node, empile
                current_children.append((node_num, num_child, num_meta))

        return self

    def payload(self):
        return sum(sum(n[1]['payload']) for n in self.G.nodes(data=True))

    def value(self, node):
        children = sorted(self.G.successors(node))
        payload = self.G.node[node]['payload']
        if children:
            value = sum(self.value(children[i-1]) for i in payload if i <= len(children))
        else:
            value = sum(payload)
        return value


# That's handy, the Advent of Code gives unittests.
def testOne():
    ex = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    ex2 = "2 3 1 1 0 1 10 1 1 2 0 1 99 1 1 1 1 2"

    print("Test {inp} gives {res}".format(inp=ex2, res=partOne(ex2)))


def testTwo():
    ex = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))

    ex2 = "2 3 1 1 0 1 10 1 1 2 0 1 99 1 1 1 1 2"

    print("Test {inp} gives {res}".format(inp=ex2, res=partTwo(ex2)))


def partOne(inp):
    license = LicenseTree.fromDescription(inp)
    return license.payload()


def partTwo(inp):
    license = LicenseTree.fromDescription(inp)
    return license.value(1)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print("")
        testTwo()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
