import re
import networkx as nx


def manhattan(p1, p2):
    return sum(map(lambda t: abs(t[0]-t[1]), zip(p1, p2)))


def toGraph(inp):
    num_re = re.compile(r"(-?\d+)")
    parsed_inp = []
    for line in inp.split('\n'):
        parsed_inp.append(tuple(map(int, num_re.findall(line))))

    G = nx.Graph()
    for i, line in enumerate(parsed_inp):
        for j in range(i):
            line2 = parsed_inp[j]
            if manhattan(line, line2) <= 3:
                G.add_edge(line, line2)
        G.add_node(line)
    return G


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp1 = """0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0"""
    res1 = partOne(inp1)
    print(f"First example test has {res1} constellations.")

    inp2 = """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""
    res2 = partOne(inp2)
    print(f"Second example test has {res2} constellations.")

    inp3 = """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2"""
    res3 = partOne(inp3)
    print(f"Third example test has {res3} constellations.")

    inp4 = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""
    res4 = partOne(inp4)
    print(f"Fourth example test has {res4} constellations.")


def testTwo():
    print("Unit test for Part Two.")

    inp = "toto"
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")


def partOne(inp):
    G = toGraph(inp)
    return nx.number_connected_components(G)


def partTwo(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
