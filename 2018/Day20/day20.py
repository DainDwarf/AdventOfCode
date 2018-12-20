import networkx as nx
#TODO: Add the display of the maze, I guess.


def parse(inp):
    """Fortunately, its much easier than it seems, because each branch of
    choices in parentheses lead to the same position, in fact."""
    G = nx.Graph()
    x = 0
    y = 0
    branches = []
    for char in inp[1:-1]:
        if char == "W":
            G.add_edge((x, y), (x-1, y))
            x = x-1
        elif char == "E":
            G.add_edge((x, y), (x+1, y))
            x = x+1
        elif char == "S":
            G.add_edge((x, y), (x, y-1))
            y = y-1
        elif char == "N":
            G.add_edge((x, y), (x, y+1))
            y = y+1
        elif char == "(":
            branches.append((x, y))
        elif char == "|":
            x, y = branches[-1]
        elif char == ")":
            branches.pop(-1)
    return G


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = "^WNE$"
    res = partOne(inp)
    print(f"Test {inp} gives {res}")

    inp = "^ENWWW(NEEE|SSE(EE|N))$"
    res = partOne(inp)
    print(f"Test {inp} gives {res}")

    inp = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
    res = partOne(inp)
    print(f"Test {inp} gives {res}")

    inp = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
    res = partOne(inp)
    print(f"Test {inp} gives {res}")

    inp = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"
    res = partOne(inp)
    print(f"Test {inp} gives {res}")


def testTwo():
    print("No unit test for Part Two!")


def partOne(inp):
    G = parse(inp)
    return nx.eccentricity(G, (0, 0))


def partTwo(inp):
    G = parse(inp)
    all_paths = nx.shortest_path_length(G, source=(0, 0))
    far_rooms = [r for r, l in all_paths.items() if l>=1000]
    return len(far_rooms)


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
