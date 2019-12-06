import pytest
import networkx as nx
from networkx.algorithms.dag import ancestors
from networkx.algorithms.shortest_paths.generic import shortest_path

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L", 42),
])
def testOne(inp, exp):
    res = partOne(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN", 4),
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


def partOne(inp):
    orbits = nx.DiGraph()
    for orbit in inp.split('\n'):
        center, orb = orbit.strip().split(')')
        orbits.add_edge(center, orb)
    return sum(len(ancestors(orbits, n)) for n in orbits.nodes)


def partTwo(inp):
    orbits = nx.Graph()
    for orbit in inp.split('\n'):
        center, orb = orbit.strip().split(')')
        orbits.add_edge(center, orb)
    # -3, because you substract YOU and SAN, and you need to count interval, not nodes.
    return len(shortest_path(orbits, 'YOU', 'SAN')) - 3


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
